import os
import warnings
import logging
from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
)

# ---- 基本設定 ----
warnings.filterwarnings("ignore", category=DeprecationWarning)

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

app = Flask(__name__)

# ---- LINE Bot 設定 ----
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# ---- Router ----
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

import firebase_admin
from firebase_admin import credentials, firestore

print("✅ Firebase Admin SDK 已安裝成功")

# ---- 加好友事件 (FollowEvent) ----
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
        )
    )
    line_bot_api.reply_message(event.reply_token, quick_reply)


# ---- 一般訊息處理 ----
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()

    if msg == "我是買家":
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "太好了！🎯", "weight": "bold", "size": "lg"},
                    {
                        "type": "text",
                        "text": "我能幫你推薦合適的房子、安排看房\n也能依你的需求推薦物件",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md",
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
                        "color": "#00C300",
                        "action": {
                            "type": "uri",
                            "label": "設定訂閱條件",
                            "uri": "https://liff.line.me/2007821360-8WJy7BmM",
                        },
                    }
                ],
            },
        }
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="設定訂閱條件", contents=flex_message),
        )

    elif msg == "我是賣家":
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "感謝您！🏠", "weight": "bold", "size": "lg"},
                    {
                        "type": "text",
                        "text": "想出售房子嗎？請填寫表單留下物件資訊，我會盡快與您聯絡！",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md",
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
                        "color": "#FF8000",
                        "action": {
                            "type": "uri",
                            "label": "填寫出售表單",
                            "uri": "https://real-estate-agent-test.onrender.com/sell",
                        },
                    }
                ],
            },
        }
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="出售房屋表單", contents=flex_message),
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇『我是買家』或『我是賣家』"),
        )


# ---- 表單頁面 (買家設定需求) ----
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    budget = request.form.get("budget")
    location = request.form.get("location")
    size = request.form.get("size")

    print("表單收到：", budget, location, size)
    return "已收到您的設定！"


# ---- 啟動伺服器 ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
