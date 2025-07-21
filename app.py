from flask import Flask, request, abort
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
import os

app = Flask(__name__)

# 替換成你的 LINE 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "你的AccessToken")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "你的Secret")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 替換為你的 Firebase 設定
FIREBASE_PROJECT_ID = "house-c82d9"
FIREBASE_DB_URL = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"

@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    if msg == "找好屋":
        houses = query_houses("agent001")
        if houses:
            flex = build_flex_message(houses[0])
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="推薦物件", contents=flex)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前無推薦物件，歡迎留言需求！")
            )
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入『找好屋』來獲得推薦物件"))

def query_houses(agent_id):
    url = f"{FIREBASE_DB_URL}/users/{agent_id}/house"
    res = requests.get(url)
    if res.status_code != 200:
        return []
    data = res.json()
    documents = data.get("documents", [])
    houses = []
    for doc in documents:
        fields = doc.get("fields", {})
        house = {
            "title": fields.get("title", {}).get("stringValue", "無標題"),
            "district": fields.get("district", {}).get("stringValue", "未知區域"),
            "price": fields.get("price", {}).get("integerValue", "0"),
            "imageUrl": fields.get("imageUrl", {}).get("stringValue", ""),
            "link": fields.get("link", {}).get("stringValue", "#")
        }
        houses.append(house)
    return houses

def build_flex_message(house):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": house["imageUrl"],
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": house["title"], "weight": "bold", "size": "lg", "wrap": True},
                {"type": "text", "text": f"地區：{house['district']}", "size": "sm", "color": "#666666"},
                {"type": "text", "text": f"總價：{house['price']} 萬", "size": "sm", "color": "#666666"}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "uri",
                        "label": "查看詳情",
                        "uri": house["link"]
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    app.run(debug=True)
