import os
import logging
import warnings
from flask import Flask, request, abort, render_template, jsonify
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
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# ---- Router ----
@app.route("/", methods=["GET"])
def index():
    return "✅ LINE Bot is running."


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, "❌ Invalid signature")

    return "OK"


# ---- 加好友事件 (FollowEvent) ----
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_text = (
        "歡迎加入張大彬的 LINE！🎉\n\n"
        "我可以協助你：\n"
        "✔ 找適合的房子\n"
        "✔ 分析物件行情\n"
        "✔ 協助你賣房找買家\n\n"
        "👉 請選擇您的身分："
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
        reply_flex_message(event, "太好了！🎯", "我能幫你推薦合適的房子、安排看房\n也能依你的需求推薦物件",
                           "設定訂閱條件", "https://real-estate-agent-test.onrender.com/setting", "#00C300")

    elif msg == "我是賣家":
        reply_flex_message(event, "感謝您！🏠", "想出售房子嗎？請填寫表單留下物件資訊，我會盡快與您聯絡！",
                           "填寫出售表單", "https://real-estate-agent-test.onrender.com/sell", "#FF8000")

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="⚠️ 請選擇『我是買家』或『我是賣家』")
        )


def reply_flex_message(event, title, description, button_label, button_uri, button_color):
    """共用 Flex Message 回覆"""
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": title, "weight": "bold", "size": "lg"},
                {"type": "text", "text": description, "size": "sm", "wrap": True, "margin": "md"},
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "color": button_color,
                    "action": {"type": "uri", "label": button_label, "uri": button_uri},
                }
            ],
        },
    }

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text=button_label, contents=flex_message)
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

    # ✅ 回傳 JSON，方便前端或 LIFF 顯示成功訊息
    return jsonify({
        "status": "success",
        "message": "已收到您的設定！",
        "data": {
            "budget": budget,
            "location": location,
            "size": size
        }
    })


# ---- 啟動伺服器 ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
