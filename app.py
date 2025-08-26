import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FollowEvent, QuickReply, QuickReplyButton, MessageAction
)

app = Flask(__name__)

# 從環境變數讀取 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

# 健康檢查
@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

# LINE Webhook
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    for event in events:
        if  isinstance(event, FollowEvent):
            # 用 QuickReply 引導身份
            quick_reply = TextSendMessage(
                text="歡迎加入張大彬的 LINE！\n"
                     "我可以協助你：\n"
                     "✔ 找適合的房子\n"
                     "✔ 分析物件行情\n"
                     "✔ 協助你賣房找買家！\n"
                     "請選擇您的身分：",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(label="我是買家", text="我是買家")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="我是賣家", text="我是賣家")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="先看市場", text="我先觀望市場")
                        ),
                    ]
                )
            )
            line_bot_api.reply_message(event.reply_token, quick_reply)

    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render/Heroku 會自動給 PORT
    app.run(host="0.0.0.0", port=port)
