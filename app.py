import os
import json
import logging
import warnings
from flask import Flask, request, abort, render_template, jsonify

# LINE SDK
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
)

# dotenv
from dotenv import load_dotenv

# -------------------- 載入環境變數 --------------------
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
LIFF_ID = os.getenv("LIFF_ID", "2007821360-8WJy7BmM")
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

# -------------------- 小工具 --------------------
def extract_form_data():
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

# -------------------- 路由 --------------------
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

    log.info(f"[callback] body={body}")

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        log.warning("[callback] 簽名驗證失敗")
        abort(400)
    except Exception as e:
        log.exception("[callback] handler error")
        abort(500)

    return "OK"

# -------------------- FollowEvent --------------------
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_text = (
        "歡迎加入張大彬的 LINE！\n"
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

# -------------------- 簡單訊息測試 --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    log.info(f"[handle_message] 收到訊息: {repr(msg)}")

    # 測試用，確保 webhook 正常
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"您傳了：{msg}")
    )

# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

@app.route("/search", methods=["GET"])
def show_search_form():
    return render_template("search_form.html")

# -------------------- 表單提交 --------------------
@app.route("/submit_form", methods=["POST"])
def submit_form():
    try:
        data = extract_form_data()
        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        doc_ref = db.collection("forms").document(user_id)
        existed = doc_ref.get().exists
        payload = {
            "budget": budget, "room": room, "genre": genre, "user_id": user_id,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        if not existed:
            payload["created_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.set(payload, merge=True)

        return jsonify({"status": "success"})
    except Exception as e:
        log.exception(f"[submit_form] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# -------------------- 分享頁面 --------------------
firebase_config = {
    "apiKey": "你的-APIKEY",
    "authDomain": "real-estate-agent-test-d1300.firebaseapp.com",
    "projectId": "real-estate-agent-test-d1300",
    "storageBucket": "real-estate-agent-test-d1300.firebasestorage.app",
    "messagingSenderId": "865490826137",
    "appId": "1:865490826137:web:6cc1ef99202edc58e8d908",
    "measurementId": "G-NPTDMJE5K2"
}

@app.route("/share/<listing_id>")
def share(listing_id):
    return render_template("share.html", listing_id=listing_id, firebase_config=firebase_config)

# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
