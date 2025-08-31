# app.py
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

# Firebase Admin
import firebase_admin
from firebase_admin import credentials, firestore

# -------------------- 基本設定 --------------------
warnings.filterwarnings("ignore", category=DeprecationWarning)
logging.basicConfig(level=logging.INFO)
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
        raise RuntimeError("缺少 FIREBASE_CREDENTIALS 環境變數")
    cred = credentials.Certificate(json.loads(raw_json))
    firebase_admin.initialize_app(cred)

db = firestore.client()
app.logger.info("✅ Firebase 初始化成功")

# -------------------- Flex 建構函式 --------------------
def build_condition_card(title, budget, room, genre, liff_url):
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

def build_intro_card():
    return {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "mega",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1753039495/大彬看房_頭貼_工作區域_1_addzrg.jpg"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "張大彬 Leo", "weight": "bold", "align": "center", "size": "xl"},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [{"type": "text", "text": "新世代自媒體", "color": "#7B7B7B"}],
                                    "backgroundColor": "#D0D0D0",
                                    "cornerRadius": "5px",
                                    "height": "23px",
                                    "justifyContent": "center",
                                    "alignItems": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [{"type": "text", "text": "優質資深房仲", "color": "#7B7B7B"}],
                                    "backgroundColor": "#D0D0D0",
                                    "cornerRadius": "5px",
                                    "height": "23px",
                                    "justifyContent": "center",
                                    "alignItems": "center"
                                }
                            ],
                            "justifyContent": "space-between"
                        },
                        {"type": "text", "text": "桃園市中壢區", "size": "lg", "weight": "bold", "color": "#FF8000", "margin": "md"},
                        {
                            "type": "text",
                            "text": "擁有多年的房地產經驗\n也經營 TikTok、YouTube 分享房市趨勢與生活趣事\n\n想買房、換屋，或了解市場，都歡迎與我聊聊！",
                            "size": "sm",
                            "wrap": True,
                            "margin": "md"
                        },
                        {"type": "separator", "color": "#101010", "margin": "md"},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "button",
                                    "style": "primary",
                                    "color": "#FF8000",
                                    "action": {"type": "uri", "label": "用影片更認識我", "uri": "https://www.tiktok.com/@leochang9453"}
                                },
                                {
                                    "type": "button",
                                    "style": "secondary",
                                    "color": "#7B7B7B",
                                    "action": {"type": "uri", "label": "通話", "uri": "tel:0918837739"}
                                }
                            ],
                            "justifyContent": "space-between",
                            "margin": "md"
                        }
                    ]
                }
            }
        ]
    }

# -------------------- 路由 --------------------
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
    app.logger.info(f"📩 收到訊息: {msg}")

    if msg == "我是買家":
        flex_message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "太好了！🎯", "weight": "bold", "size": "lg"},
                    {"type": "text", "text": "我能幫你推薦合適的房子、安排看房\n也能依你的需求推薦物件", "size": "sm", "wrap": True, "margin": "md"}
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
                        "action": {"type": "uri", "label": "設定訂閱條件", "uri": LIFF_URL},
                    }
                ],
            },
        }
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="設定訂閱條件", contents=flex_message))

    elif msg == "我是賣家":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="📋 請前往表單填寫出售資料：\nhttps://你的網域/sell"))

    elif msg == "管理我的追蹤條件":
        flex_message = build_condition_card("🔧 修改追蹤條件", "-", "-", "-", LIFF_URL)
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="修改追蹤條件", contents=flex_message))

    elif msg == "你是誰":
        flex_message = build_intro_card()
        line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="我是誰", contents=flex_message))

# -------------------- 表單處理 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

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
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        doc_ref = db.collection("forms").document(user_id)
        existed = doc_ref.get().exists
        payload = {"budget": budget, "room": room, "genre": genre, "user_id": user_id, "updated_at": firestore.SERVER_TIMESTAMP}
        if not existed:
            payload["created_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.set(payload, merge=True)

        title = "🎉 用戶第一次填表單，追蹤成功！" if not existed else "✅ 追蹤條件已更新！"
        flex_message = build_condition_card(title, budget, room, genre, LIFF_URL)

        try:
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=flex_message))
            app.logger.info(f"[submit_form] 已推播給 {user_id}")
        except Exception as e:
            app.logger.exception(f"[submit_form] push_message 失敗: {e}")

        return jsonify({"status": "success", "message": "saved & pushed"})
    except Exception as e:
        app.logger.exception(f"[submit_form] 錯誤: {e}")
        return jsonify({"status": "error", "message": "internal error"}), 500

# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
