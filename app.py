# app.py
import os
import json
import logging
import warnings

from flask import Flask, request, abort, render_template, jsonify

# Flex 模板模組（與 app.py 同層）
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
app = Flask(__name__)


# -------------------- 環境變數 --------------------
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
LIFF_URL = os.getenv("LIFF_URL", "https://liff.line.me/2007821360-8WJy7BmM")

if not LINE_CHANNEL_ACCESS_TOKEN or not LINE_CHANNEL_SECRET:
    raise ValueError("請先設定 LINE_CHANNEL_ACCESS_TOKEN 與 LINE_CHANNEL_SECRET 環境變數")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# -------------------- Firebase 初始化（使用環境變數 JSON） --------------------
if not firebase_admin._apps:
    raw_json = os.getenv("FIREBASE_CREDENTIALS")
    if not raw_json:
        raise RuntimeError("缺少環境變數 FIREBASE_CREDENTIALS（請填入完整的 service account JSON）")
    cred = credentials.Certificate(json.loads(raw_json))
    firebase_admin.initialize_app(cred)

db = firestore.client()
app.logger.info("✅ Firebase 已初始化成功")


# -------------------- 共用：回推追蹤條件卡片（給 submit_form 用） --------------------
def build_condition_card(title: str, budget: str, room: str, genre: str, liff_url: str):
    """用於 submit_form 成功後回推目前追蹤條件。"""
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


# -------------------- 健康檢查 / 首頁 --------------------
@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running."

@app.route("/healthz", methods=["GET"])
def healthz():
    return "ok"


# -------------------- LINE Webhook 入口 --------------------
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"


# -------------------- FollowEvent：歡迎訊息 + 快速回覆 --------------------
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


# -------------------- 一般訊息處理 --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    app.logger.info(f"📩 收到訊息: {msg}")

    if msg == "我是買家":
        # Flex：導去 LIFF 表單設定條件
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="設定訂閱條件", contents=ft.buyer_card(LIFF_URL))
        )

    elif msg == "我是賣家":
        # 純文字：導去賣屋表單（可改為 Flex）
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ft.seller_text())
        )

    elif msg == "管理我的追蹤條件":
        # Flex：管理/修改追蹤條件
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="修改追蹤條件", contents=ft.manage_condition_card(LIFF_URL))
        )

    elif msg == "你是誰":
        # Flex：個人介紹
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我是誰", contents=ft.intro_card())
        )

    else:
        # 其他訊息：回聲（可改你的預設流程）
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"你剛剛說：{msg}")
        )


# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    # 確保 templates/setting_form.html 存在
    return render_template("setting_form.html")


# -------------------- 表單提交（LIFF 回傳） --------------------
@app.route("/submit_form", methods=["GET", "POST"])
def submit_form():
    try:
        # 直接 GET 避免誤觸
        if request.method == "GET":
            return jsonify({"status": "error", "message": "use POST"}), 405

        # 取得 LIFF 表單欄位
        budget = request.form.get("budget")
        room   = request.form.get("room")
        genre  = request.form.get("genre")
        user_id = request.form.get("user_id")

        app.logger.info(f"[submit_form] POST budget={budget}, room={room}, genre={genre}, user_id={user_id}")

        # 基本驗證
        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id from LIFF"}), 400

        # 以 user_id 當 doc id（存在則更新、否則建立）
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

        # 推播回 LINE：顯示目前追蹤條件
        title = "🎉 用戶第一次填表單，追蹤成功！" if not existed else "✅ 追蹤條件已更新！"
        card = build_condition_card(title, budget, room, genre, LIFF_URL)

        try:
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))
            app.logger.info(f"[submit_form] 已推播給 {user_id}")
        except Exception as e:
            app.logger.exception(f"[submit_form] push_message 失敗: {e}")

        return jsonify({"status": "success", "message": "saved to Firestore & pushed LINE"})

    except Exception as e:
        app.logger.exception(f"[submit_form] 未預期錯誤: {e}")
        return jsonify({"status": "error", "message": "internal error"}), 500


# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
