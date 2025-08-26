from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數讀取 LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 健康檢查
@app.route("/", methods=["GET"])
def home():
    return "LINE Bot is running!"

# LINE Webhook
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("Webhook Error:", e)
        abort(400)

    return "OK"

# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_msg = event.message.text
    reply = f"你剛剛說：{user_msg}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render/Heroku 會自動給 PORT
    app.run(host="0.0.0.0", port=port)

@handler.add(FollowEvent)
def handle_follow(event):
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
            ])
        )
    line_bot_api.reply_message(event.reply_token, quick_reply)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()


if __name__ == "__main__":
    app.run(debug=True)
