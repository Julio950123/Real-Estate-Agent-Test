# seed_listings.py
import os, json, csv, firebase_admin
from firebase_admin import credentials, firestore

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

def to_number(x):
    try:
        if x is None or x == "": return None
        return float(x) if "." in str(x) else int(x)
    except Exception:
        return None

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
            "title": item.get("title", "").strip(),
            "price": to_number(item.get("price")),
            "room": to_number(item.get("room")),
            "genre": item.get("genre", "").strip(),
            "address": item.get("address", "").strip(),
            "image_url": item.get("image_url", "").strip(),
            "square_meters": to_number(item.get("square_meters")),
            "detail1": item.get("detail1", "").strip(),
            "detail2": item.get("detail2", "").strip(),
            "status": item.get("status", "active"),
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
