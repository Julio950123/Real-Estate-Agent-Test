import os
import json
import logging
import warnings
from urllib.parse import parse_qs
from flask import Flask, request, abort, render_template, jsonify

# -------------------- LINE SDK --------------------
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction,
    PostbackEvent
)

# -------------------- dotenv --------------------
from dotenv import load_dotenv
if os.path.exists(".env.local"):
    load_dotenv(".env.local", override=True)

APP_ENV = os.getenv("APP_ENV", "local")
if APP_ENV == "prod":
    print("🚀 使用 .env.prod 設定")
    if os.path.exists(".env.prod"):
        load_dotenv(".env.prod", override=True)
else:
    print("🛠 使用 .env.local 設定")

# -------------------- 讀取 LINE 設定 --------------------
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LIFF_ID = os.getenv("LIFF_ID", "")
LIFF_URL = f"https://liff.line.me/{LIFF_ID}"

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("❌ 請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

# -------------------- 基本設定 --------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# -------------------- Firebase 初始化 --------------------
import firebase_admin
from firebase_admin import credentials, firestore

if not firebase_admin._apps:
    raw_json = os.getenv("FIREBASE_CREDENTIALS")
    raw_file = os.getenv("FIREBASE_CREDENTIALS_FILE")
    try:
        if raw_json:
            cred = credentials.Certificate(json.loads(raw_json))
            log.info("✅ 使用 FIREBASE_CREDENTIALS JSON 初始化成功")
        elif raw_file and os.path.exists(raw_file):
            cred = credentials.Certificate(raw_file)
            log.info(f"✅ 使用 FIREBASE_CREDENTIALS_FILE ({raw_file}) 初始化成功")
        else:
            raise RuntimeError("❌ 缺少 FIREBASE_CREDENTIALS 或 FIREBASE_CREDENTIALS_FILE")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        log.exception("❌ Firebase 初始化失敗")
        raise

db = firestore.client()

# -------------------- 物件搜尋函式 --------------------
def search_listings(keyword: str):
    """搜尋 listings，TOP 物件優先"""
    query = db.collection("listings") \
        .where("title", ">=", keyword) \
        .where("title", "<=", keyword + "\uf8ff") \
        .order_by("top", direction=firestore.Query.DESCENDING)

    return query.stream()

# -------------------- API 路由 --------------------
@app.route("/search", methods=["GET"])
def search():
    """搜尋 API：?q=關鍵字"""
    keyword = request.args.get("q", "").strip()
    if not keyword:
        return jsonify({"status": "error", "message": "missing keyword"}), 400

    results = search_listings(keyword)

    data = []
    for doc in results:
        item = doc.to_dict()
        item["id"] = doc.id  # 加上 document ID
        data.append(item)

    return jsonify({"status": "ok", "results": data})


# -------------------- top關鍵字物件 --------------------
from linebot.models import FlexSendMessage, TextSendMessage

def get_top_flex():
    """抓取 top==True 的物件，組合成 carousel"""
    docs = db.collection("listings").where("top", "==", True).limit(5).stream()  # 限制最多5筆

    bubbles = []
    for doc in docs:
        data = doc.to_dict()
        bubble = listing_card(doc.id, data)   # 🔥 用你提供的 Flex 樣板函式
        bubbles.append(bubble)

    if not bubbles:
        return None

    return {
        "type": "carousel",
        "contents": bubbles
    }

# -------------------- LINE Bot MessageEvent --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()

    if text == "中壢夜市生活圈精選":  # 輸入關鍵字就抓 TOP 物件
        flex = get_top_flex()
        if flex:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="精選物件", contents=flex)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前沒有精選物件 🙏")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"你輸入的是：{text}")
        )

# -------------------- 工具函式 --------------------
def build_condition_card(title: str, budget: str, room: str, genre: str, liff_url: str):
    """管理追蹤條件卡片"""
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "5px",
            "contents": [
                {"type": "text", "text": title, "weight": "bold", "size": "md", "color": "#101010"},
                {"type": "separator", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "lg", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "lg", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "lg", "wrap": True},
                    ],
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "height": "sm",
                    "color": "#EB941E",
                    "action": {"type": "uri", "label": "更改追蹤條件", "uri": liff_url},
                }
            ],
        },
    }

def extract_form_data():
    """同時支援 JSON 與 form-urlencoded"""
    try:
        if request.is_json:
            data = request.get_json(force=True)
            log.info(f"[extract_form_data] 收到 JSON: {data}")
            return data
        else:
            data = request.form.to_dict()
            log.info(f"[extract_form_data] 收到 form-data: {data}")
            return data
    except Exception as e:
        log.exception(f"[extract_form_data] 解析失敗: {e}")
        return {}

# -------------------- 基礎路由 --------------------
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."

@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok"

# -------------------- LINE Webhook --------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# -------------------- FollowEvent --------------------
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_text = (
        "我可以協助你：\n"
        "✔ 找適合的房子\n"
        "✔ 分析物件行情\n"
        "✔ 協助你賣房找買家！\n\n"
        "請選擇您的需求："
    )
    quick_reply = TextSendMessage(
        text=welcome_text,
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="我想買房", text="我想買房")),
                QuickReplyButton(action=MessageAction(label="委託賣房", text="委託賣房")),
                QuickReplyButton(action=MessageAction(label="立即找房", text="立即找房")),
            ]
        ),
    )
    line_bot_api.reply_message(event.reply_token, quick_reply)

# -------------------- 一般訊息 --------------------
import flex_templates as ft

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    log.info(f"[handle_message] 收到訊息: {repr(msg)}")

    if msg == "我想買房":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我想買房", contents=ft.buyer_card(LIFF_URL))
        )
    elif msg == "委託賣房":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ft.seller_text()))
    elif msg == "立即找房":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="立即找房", contents=ft.search_card())
        )
    elif msg == "你是誰":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="你是誰", contents=ft.intro_card())
        )
    elif msg == "管理我的追蹤條件":
        user_id = event.source.user_id
        doc = db.collection("forms").document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            budget = data.get("budget", "-")
            room = data.get("room", "-")
            genre = data.get("genre", "-")
        else:
            budget, room, genre = "-", "-", "-"
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="管理我的追蹤條件",
                contents=ft.manage_condition_card(budget, room, genre, LIFF_URL)
            )
        )

# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

@app.route("/search", methods=["GET"])
def show_search_form():
    return render_template("search_form.html")

@app.route("/share")
def share_page():
    """LIFF 分享頁面"""
    return render_template("share.html")

# -------------------- 表單提交 --------------------
@app.route("/submit_form", methods=["POST"])
def submit_form():
    """訂閱條件提交"""
    try:
        data = request.get_json(force=True, silent=True) or request.form.to_dict()
        log.info(f"[submit_form] 收到資料: {data}")

        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        doc_ref = db.collection("forms").document(user_id)
        existed = doc_ref.get().exists

        payload = {
            "budget": budget,
            "room": room,
            "genre": genre,
            "user_id": user_id,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        if not existed:
            payload["created_at"] = firestore.SERVER_TIMESTAMP

        doc_ref.set(payload, merge=True)

        # 回傳 Flex
        title = "🎉 追蹤成功！" if not existed else "條件已更新"
        card = build_condition_card(title, budget, room, genre, LIFF_URL)
        line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))

        return jsonify({"status": "success"})
    except Exception as e:
        log.exception(f"[submit_form] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/submit_search", methods=["POST"])
def submit_search():
    """立即找房提交"""
    try:
        data = request.get_json(force=True, silent=True) or request.form.to_dict()
        log.info(f"[submit_search] 收到資料: {data}")

        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        # 儲存 search_log
        db.collection("search_form").document().set({
            "budget": budget,
            "room": room,
            "genre": genre,
            "user_id": user_id,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        # 查 listings
        query = db.collection("listings")
        if budget and budget.isdigit() and int(budget) > 0:
            query = query.where("price", "<=", int(budget))
        if room and room.isdigit() and int(room) > 0:
            query = query.where("room", "==", int(room))
        if genre and genre != "不限":
            query = query.where("genre", "==", genre)

        docs = query.limit(5).stream()
        bubbles = [ft.listing_card(doc.id, doc.to_dict()) for doc in docs]

        if bubbles:
            carousel = {"type": "carousel", "contents": bubbles}
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text="找到物件", contents=carousel))
        else:
            line_bot_api.push_message(user_id, TextSendMessage(text="❌ 沒有符合的物件"))

        return jsonify({"status": "success"})
    except Exception as e:
        log.exception(f"[submit_search] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------- PostbackEvent (物件詳情) --------------------
from flex_templates import property_flex

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    params = parse_qs(data)
    action = params.get("action", [None])[0]
    house_id = params.get("id", [None])[0]

    if action == "detail" and house_id:
        doc = db.collection("listings").document(house_id).get()
        if not doc.exists:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="❌ 找不到物件資訊"))
            return

        house = doc.to_dict()
        flex_json = ft.property_flex(house_id, house)

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text=f"物件詳情：{house.get('title', '')}",
                contents=flex_json
            )
        )


# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
