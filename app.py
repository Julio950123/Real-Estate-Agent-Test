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
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "5px",
            "contents": [
                {"type": "text", "text": title, "weight": "bold", "size": "md", "color": "#101010"},
                {"type": "separator", "margin": "sm"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "md", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "md", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "md", "wrap": True},
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
                    "height": "sm",
                    "color": "#EB941E",
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
        "請選擇您的需求："
    )
    quick_reply = TextSendMessage(
        text=welcome_text,
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="我想買房", text="我想買房")),
                QuickReplyButton(action=MessageAction(label="委託賣房", text="委託賣房")),
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

    if "我想買房" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我想買房", contents=ft.buyer_card(LIFF_URL))
        )

    elif "委託賣房" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ft.seller_text())
        )

    elif "管理我的追蹤條件" in msg :
        user_id = event.source.user_id
        doc_ref = db.collection("forms").document(user_id).get()
        data = doc_ref.to_dict() if doc_ref.exists else {}

        budget = data.get("budget", "-")
        room = data.get("room", "-")
        genre = data.get("genre", "-")

        card = ft.manage_condition_card(budget, room, genre, LIFF_URL)

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="修改追蹤條件", contents=card)
        )

    elif "你是誰" in msg:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="你是誰", contents=ft.intro_card)
        )

    elif msg.startswith("找房"):
        keyword = msg.replace("找房", "").strip()

        docs = db.collection("listings")\
            .where("title", ">=", keyword)\
            .where("title", "<=", keyword + "\uf8ff")\
            .stream()

        bubbles = [ft.listing_card(doc.to_dict()) for doc in docs]

        if bubbles:
            carousel = {"type": "carousel", "contents": bubbles[:5]}  # 最多 5 筆
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="找到物件", contents=carousel)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="❌ 沒找到符合的物件")
            )


# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

# -------------------- 表單提交 --------------------
from flask import request, jsonify, render_template_string, redirect, url_for

LIFF_ID = "2007821360-8WJy7BmM"   # 記得填你的 LIFF ID
LIFF_URL = "https://liff.line.me/2007821360-8WJy7BmM"  # 你原本就有用到

@app.route("/submit_form", methods=["POST"])
def submit_form():
    try:
        # --- 1) 同時支援 JSON 與 form-urlencoded ---
        if request.is_json:  # fetch(JSON)
            data   = request.get_json(force=True)
            budget = data.get("budget")
            room   = data.get("room")
            genre  = data.get("genre")
            user_id= data.get("user_id")
            is_ajax = True
        else:                # 傳統 <form>
            budget = request.form.get("budget")
            room   = request.form.get("room")
            genre  = request.form.get("genre")
            user_id= request.form.get("user_id")
            is_ajax = False

        app.logger.info(f"[submit_form] budget={budget}, room={room}, genre={genre}, user_id={user_id}")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id from LIFF"}), 400

        # --- 2) Firestore 儲存 ---
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

        # --- 3) 推送 LINE 卡片（失敗時不阻斷流程） ---
        title = "已追蹤成功！當前追蹤條件" if not existed else "已更改成功！當前追蹤條件"
        card = build_condition_card(title, budget, room, genre, LIFF_URL)
        try:
            line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))
            app.logger.info(f"[submit_form] pushed to {user_id}")
        except Exception as e:
            app.logger.exception(f"[submit_form] push_message failed: {e}")

        # --- 4) 依提交方式回應 ---
        if is_ajax:
            # ✅ AJAX/JSON：回 204，前端負責 liff.closeWindow()
            return "", 204
        else:
            # ✅ 傳統 form：回帶 LIFF SDK 的關窗頁（在 LIFF 內一定能關）
            html = f"""
            <!doctype html><html><head>
              <meta charset="utf-8" />
              <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
            </head><body>
              <script>
                (async () => {{
                  try {{
                    await liff.init({{ liffId: "{LIFF_ID}" }});
                    if (liff.isInClient()) {{
                      liff.closeWindow();
                    }} else {{
                      window.close();
                      location.href = "/thank-you";
                    }}
                  }} catch (e) {{
                    window.close();
                    location.href = "/thank-you";
                  }}
                }})();
              </script>
            </body></html>
            """
            return render_template_string(html)

    except Exception as e:
        app.logger.exception(f"[submit_form] unhandled error: {e}")
        return jsonify({"status": "error", "message": "internal error"}), 500


# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
