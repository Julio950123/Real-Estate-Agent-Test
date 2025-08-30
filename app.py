import os
import warnings
import logging
import json
from flask import Flask, request, abort, render_template, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    FlexSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
)

import firebase_admin
from firebase_admin import credentials, firestore

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

# ---- Firebase 初始化（從環境變數讀取 JSON）----
if not firebase_admin._apps:
    firebase_config = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
    cred = credentials.Certificate(firebase_config)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase 已初始化成功")


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
                            "uri": "https://liff.line.me/2007821360-8WJy7BmM",  # ⚠️ 改成你的 LIFF 表單網址
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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="📋 請前往表單填寫出售資料：\nhttps://你的網域/sell")
        )

    elif msg == "管理我的追蹤條件":
        flex_message = {
            "type": "bubble",
            "size": "micro",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🔧 修改追蹤條件",
                        "weight": "bold",
                        "size": "md",
                        "color": "#333333"
                    },
                    {
                        "type": "text",
                        "text": "點擊下方按鈕即可更新你的訂閱需求",
                        "size": "sm",
                        "wrap": True,
                        "margin": "md"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#0066FF",
                        "action": {
                            "type": "uri",
                            "label": "修改追蹤條件",
                            "uri": "https://liff.line.me/2007821360-8WJy7BmM"  # ⚠️ 改成你的 LIFF 表單網址
                        }
                    }
                ]
            }
        }

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="修改追蹤條件", contents=flex_message),
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇『我是買家』或『我是賣家』"),
        )


# ---- 表單頁面 ----
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")


@app.route("/submit_form", methods=["POST"])
def submit_form():
    budget = request.form.get("budget")
    room = request.form.get("room")
    genre = request.form.get("genre")
    user_id = request.form.get("user_id")

    print("📌 表單收到：", budget, room, genre, user_id)

    # Firestore: 查詢 user_id 是否已存在
    docs = db.collection("forms").where("user_id", "==", user_id).stream()
    existed = any(True for _ in docs)

    # Firestore: 新增紀錄
    db.collection("forms").add({
        "budget": budget,
        "room": room,
        "genre": genre,
        "user_id": user_id,
        "created_at": firestore.SERVER_TIMESTAMP
    })

    # ---- 組 Flex 推播 ----
    title_text = "🎉 用戶第一次填表單，追蹤成功！" if not existed else "✅ 追蹤條件已更新！"
    flex_message = {
        "type": "bubble",
        "size": "micro",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": title_text, "weight": "bold", "size": "md", "color": "#00AA00"},
                {"type": "separator", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"格局：{room}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"類型：{genre}", "size": "sm", "wrap": True},
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
                    "action": {
                        "type": "uri",
                        "label": "更改追蹤條件",
                        "uri": "https://liff.line.me/你的-LIFF-ID"  # ⚠️ 改成你的 LIFF 表單網址
                    },
                }
            ],
        },
    }

    if user_id:
        line_bot_api.push_message(
            user_id,
            FlexSendMessage(alt_text=title_text, contents=flex_message)
        )
        print("✅ 已推播給使用者:", user_id)

    return jsonify({"status": "success", "message": "已存入 Firebase 並推播到 LINE"})


# ---- 啟動伺服器 ----
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
