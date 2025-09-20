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

# -------------------- 搜尋表單頁面 --------------------
@app.route("/search", methods=["GET"])
def show_search_form():
    return render_template("search_form.html")

# -------------------- 搜尋 API (top 精選功能) --------------------
@app.route("/search_api", methods=["GET"])
def search_api():
    docs = db.collection("listings").where("top", "==", True).limit(5).stream()
    data = []
    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        data.append(item)
    return jsonify({"status": "ok", "results": data})

# -------------------- top 精選 --------------------
from linebot.models import FlexSendMessage, TextSendMessage
import flex_templates as ft

def get_top_flex():
    docs = db.collection("listings").where("top", "==", True).limit(5).stream()
    bubbles = []
    for doc in docs:
        data = doc.to_dict()
        log.info(f"[get_top_flex] 抓到資料: {doc.id} -> {data}")
        try:
            bubble = ft.listing_card(doc.id, data)
            bubbles.append(bubble)
        except Exception as e:
            log.error(f"[get_top_flex] 產生 Flex 失敗: {e}")
    if not bubbles:
        log.info("[get_top_flex] 沒有找到 top==True 的物件")
        return None
    return {"type": "carousel", "contents": bubbles}

# -------------------- LINE Bot MessageEvent --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    log.info(f"[handle_message] 收到訊息: {repr(msg)}")

    # --- TOP 精選 ---
    if msg == "中壢夜市生活圈精選":
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

    # --- 一般選單 ---
    elif msg == "我想買房":
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

# -------------------- 表單提交 --------------------
@app.route("/submit_form", methods=["POST"])
def submit_form():
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

        title = "🎉 追蹤成功！" if not existed else "條件已更新"
        card = ft.manage_condition_card(budget, room, genre, LIFF_URL)
        line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))

        return jsonify({"status": "success"})
    except Exception as e:
        log.exception(f"[submit_form] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/submit_search", methods=["POST"])
def submit_search():
    try:
        data = request.get_json(force=True, silent=True) or request.form.to_dict()
        log.info(f"[submit_search] 收到資料: {data}")

        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        db.collection("search_form").document().set({
            "budget": budget,
            "room": room,
            "genre": genre,
            "user_id": user_id,
            "created_at": firestore.SERVER_TIMESTAMP
        })

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

# -------------------- 基礎路由 --------------------
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."

@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok"

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
