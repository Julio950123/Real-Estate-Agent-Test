# app.py
import os
import json
import logging
import warnings
from flask import Flask, request, abort, render_template, jsonify
import flex_templates as ft

# LINE SDK
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
)

# Firebase Admin
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------- 基本設定 --------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")

app = Flask(__name__)

# -------------------- 環境變數 --------------------
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LIFF_URL = os.getenv("LIFF_URL", "https://liff.line.me/2007821360-8WJy7BmM")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# -------------------- Firebase 初始化 --------------------
if not firebase_admin._apps:
    raw_json = os.getenv("FIREBASE_CREDENTIALS")
    if not raw_json:
        raise RuntimeError("缺少環境變數 FIREBASE_CREDENTIALS")
    cred = credentials.Certificate(json.loads(raw_json))
    firebase_admin.initialize_app(cred)

db = firestore.client()
log.info("✅ Firebase 已初始化成功")

# -------------------- 小工具 --------------------
def build_condition_card(title: str, budget: str, room: str, genre: str, liff_url: str):
    return {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": title, "weight": "bold", "size": "md", "color": "#0a8a0a"},
                {"type": "separator", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "sm", "wrap": True},
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
                    "color": "#0066FF",
                    "action": {"type": "uri", "label": "更改追蹤條件", "uri": liff_url},
                }
            ],
        },
    }

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
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
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
        "請選擇您的身分："
    )
    quick_reply = TextSendMessage(
        text=welcome_text,
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="我是買家", text="我是買家")),
                QuickReplyButton(action=MessageAction(label="我是賣家", text="我是賣家")),
                QuickReplyButton(action=MessageAction(label="先看市場", text="先看市場")),
            ]
        ),
    )
    line_bot_api.reply_message(event.reply_token, quick_reply)

# -------------------- 一般訊息 --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    log.info(f"[handle_message] 收到訊息: {repr(msg)}")

    if "我是買家" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我是買家", contents=ft.buyer_card(LIFF_URL))
        )

    elif "我是賣家" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ft.seller_text())
        )

    elif "管理" in msg and "追蹤" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="修改追蹤條件", contents=ft.manage_condition_card(LIFF_URL))
        )

    elif "你是誰" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我是誰", contents=ft.intro_card())
        )

# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

# -------------------- 表單提交 --------------------
@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    try:
        if request.method == "GET":
            return jsonify({"status": "error", "message": "use POST"}), 405

        budget = request.form.get("budget")
        room   = request.form.get("room")
        genre  = request.form.get("genre")
        user_id = request.form.get("user_id")

        app.logger.info(f"[submit_form] POST budget={budget}, room={room}, genre={genre}, user_id={user_id}")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id from LIFF"}), 400

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

        title = "🎉 用戶第一次填表單，追蹤成功！" if not existed else "✅ 追蹤條件已更新！"
        card = build_condition_card(title, budget, room, genre, LIFF_URL)

        try:
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))
            app.logger.info(f"[submit_form] pushed to {user_id}")
        except Exception as e:
            app.logger.exception(f"[submit_form] push_message failed: {e}")

        return jsonify({"status": "success", "message": "saved to Firestore & pushed LINE"})

    except Exception as e:
        app.logger.exception(f"[submit_form] unhandled error: {e}")
        return jsonify({"status": "error", "message": "internal error"}), 500

# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
