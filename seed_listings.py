import os, json, csv, re, firebase_admin
from firebase_admin import credentials, firestore

# -------------------- 初始化 Firestore --------------------
def init_firebase():
    if firebase_admin._apps:
        return firestore.client()

    raw = os.getenv("FIREBASE_CREDENTIALS")
    file_path = os.getenv("FIREBASE_CREDENTIALS_FILE")

    if raw:
        cred = credentials.Certificate(json.loads(raw))
    elif file_path:
        cred = credentials.Certificate(file_path)
    else:
        cred = credentials.Certificate("real-estate-agent-test-d1300-firebase-adminsdk-fbsvc-7562a131ed.json")

    firebase_admin.initialize_app(cred)
    return firestore.client()


# -------------------- 工具函式 --------------------
def chinese_to_number(text: str) -> str:
    """將中文字數字轉成阿拉伯數字（僅支援 1~10，用於數字欄位）"""
    mapping = {"一": "1", "二": "2", "三": "3", "四": "4", "五": "5",
               "六": "6", "七": "7", "八": "8", "九": "9", "十": "10"}
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text


def to_number(x, default=None):
    """把字串安全轉成 int/float，只保留數字與小數點，支援中文字數字"""
    if x is None:
        return default
    try:
        s = str(x).strip()
        if s == "":
            return default
        # 僅在數字欄位處理中文字數字
        s = chinese_to_number(s)
        # 移除非數字與小數點（萬、元、房、逗號）
        cleaned = re.sub(r"[^0-9.]", "", s)
        if cleaned == "":
            return default
        return float(cleaned) if "." in cleaned else int(cleaned)
    except Exception:
        return default


def to_bool(x):
    """把字串轉成布林值"""
    if isinstance(x, bool):
        return x
    if x is None:
        return False
    return str(x).strip().lower() in ["true", "1", "yes", "y"]


def load_items(path: str):
    """讀取 CSV 或 JSON"""
    if path.endswith(".json"):
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)
    elif path.endswith(".csv"):
        items = []
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                items.append(row)
        return items
    else:
        raise ValueError("僅支援 JSON 或 CSV")


# -------------------- 主程式 --------------------
def main():
    db = init_firebase()
    path = "./listings.csv"  # ⚡ 預設讀 CSV，可改成 ./listings.json

    items = load_items(path)
    batch = db.batch()
    count = 0

    for item in items:
        doc_id = item.get("id")  # ⚠️ 必須在 CSV/JSON 有 `id` 欄位
        if not doc_id:
            print(f"⚠️ 跳過：缺少 id -> {item}")
            continue

        data = {
            # 純文字欄位（不做數字轉換）
            "title": item.get("title", "").strip(),
            "genre": item.get("genre", "").strip(),
            "address": item.get("address", "").strip(),
            "image_url": item.get("image_url", "").strip(),
            "detail1": item.get("detail1", "").strip(),
            "detail2": item.get("detail2", "").strip(),
            "status": item.get("status", "active"),
            "project_name": item.get("project_name", "").strip(),
            "exclusive": item.get("exclusive", "").strip(),
            "pattern": item.get("pattern", "").strip(),
            "old": item.get("old", "").strip(),
            "height": item.get("height", "").strip(),
            "pattern_url": item.get("pattern_url", "").strip(),
            "video_uri": item.get("video_uri", "").strip(),
            "map_uri": item.get("map_uri", "").strip(),
            "text": item.get("text", "").strip(),

            # 數字欄位（才用 to_number）
            "price": to_number(item.get("price")),   
            "room": to_number(item.get("room")),     
            "square_meters": to_number(item.get("square_meters")),
            "square_meters2": to_number(item.get("square_meters2")),

            # 布林欄位
            "top": to_bool(item.get("top")),

            # 系統欄位
            "updated_at": firestore.SERVER_TIMESTAMP,
        }

        # ✅ 用 id 當 Firestore 文件 ID，保證不會重複新增
        doc_ref = db.collection("listings").document(doc_id)
        batch.set(doc_ref, data, merge=True)
        count += 1

        if count % 450 == 0:  # Firestore batch 限制
            batch.commit()
            print(f"✅ committed {count} docs...")
            batch = db.batch()

    batch.commit()
    print(f"🎉 done, wrote/updated {count} docs")


if __name__ == "__main__":
    main()
