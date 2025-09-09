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
LIFF_ID = os.getenv("LIFF_ID", "2007821360-8WJy7BmM")
LIFF_URL = f"https://liff.line.me/{LIFF_ID}"

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

def extract_form_data():
    """同時支援 JSON 與 form-urlencoded"""
    try:
        if request.is_json:
            data = request.get_json(force=True)
            log.info(f"[extract_form_data] 收到 JSON: {data}")
            return data
        else:
            data = request.form.to_dict()
            log.info(f"[extract_form_data] 收到 form-data: {data}")
            return data
    except Exception as e:
        log.exception(f"[extract_form_data] 解析失敗: {e}")
        return {}

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
                QuickReplyButton(action=MessageAction(label="立即找房", text="立即找房")),
            ]
        ),
    )
    line_bot_api.reply_message(event.reply_token, quick_reply)

# -------------------- 一般訊息 --------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    log.info(f"[handle_message] 收到訊息: {repr(msg)}")

    if msg == "我想買房":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="我想買房", contents=ft.buyer_card(LIFF_URL))
        )

    elif msg == "委託賣房":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ft.seller_text())
        )

    elif msg == "立即找房":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="立即找房", contents=ft.search_card())
        )

    elif msg == "你是誰":
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="你是誰", contents=ft.intro_card())
        )

    elif msg == "管理我的追蹤條件":
        user_id = event.source.user_id
        doc = db.collection("forms").document(user_id).get()
        if doc.exists:
            data = doc.to_dict()
            budget = data.get("budget", "-")
            room   = data.get("room", "-")
            genre  = data.get("genre", "-")
        else:
            budget, room, genre = "-", "-", "-"

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text="管理我的追蹤條件",
                contents=ft.manage_condition_card(budget, room, genre, LIFF_URL)
            )
        )
  

# -------------------- 表單頁面 --------------------
@app.route("/setting", methods=["GET"])
def show_form():
    return render_template("setting_form.html")

@app.route("/search", methods=["GET"])
def show_search_form():
    return render_template("search_form.html")

# -------------------- 表單提交 --------------------
def extract_form_data():
    """同時支援 JSON 與 form-urlencoded"""
    if request.is_json:
        return request.get_json(force=True)
    return request.form.to_dict()

@app.route("/submit_form", methods=["POST"])
def submit_form():
    """訂閱條件提交"""
    try:
        data = extract_form_data()
        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        doc_ref = db.collection("forms").document(user_id)
        existed = doc_ref.get().exists
        payload = {
            "budget": budget, "room": room, "genre": genre, "user_id": user_id,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        if not existed:
            payload["created_at"] = firestore.SERVER_TIMESTAMP
        doc_ref.set(payload, merge=True)

        title = "🎉 追蹤成功！" if not existed else "✅ 條件已更新"
        card = build_condition_card(title, budget, room, genre, LIFF_URL)
        line_bot_api.push_message(user_id, FlexSendMessage(alt_text=title, contents=card))

        return jsonify({"status": "success"})
    except Exception as e:
        log.exception(f"[submit_form] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

from flex_templates import listings_to_carousel

@app.route("/submit_search", methods=["POST"])
def submit_search():
    try:
        data = extract_form_data()
        log.info(f"[submit_search] 收到資料: {data}")

        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id= data.get("user_id")

        if not user_id:
            log.error("[submit_search] missing user_id")
            return jsonify({"status": "error", "message": "missing user_id"}), 400

        # 儲存搜尋條件
        db.collection("search_form").document().set({
            "budget": budget,
            "room": room,
            "genre": genre,
            "user_id": user_id,
            "created_at": firestore.SERVER_TIMESTAMP
        })

        # 查詢 listings
        query = db.collection("listings")

        # 🔎 預算條件
        try:
            if budget and budget not in ["不限", "0"]:
                query = query.where("price", "<=", int(budget))
        except Exception as e:
            log.warning(f"[submit_search] 預算格式錯誤: {budget}, error={e}")

        # 🔎 格局條件
        try:
            if room and room not in ["不限", "0"]:
                query = query.where("room", "==", int(room))
        except Exception as e:
            log.warning(f"[submit_search] 格局格式錯誤: {room}, error={e}")

        # 🔎 類型條件
        if genre and genre != "不限":
            query = query.where("genre", "==", genre)

        docs = query.limit(5).stream()
        listings = [doc.to_dict() for doc in docs]

        # ✅ log 出完整資料避免中文亂碼
        import json
        log.info(f"[submit_search] 找到 {len(listings)} 筆 listings")
        log.debug(json.dumps(listings, ensure_ascii=False, indent=2))

        # 回傳 LINE 訊息
        if listings:
            from flex_templates import listings_to_carousel
            carousel = listings_to_carousel(listings)

            line_bot_api.push_message(
                user_id,
                [
                    TextSendMessage(text="您想要的理想好屋條件為…\n正在為您搜尋中 🔍"),
                    FlexSendMessage(alt_text="找到物件", contents=carousel)
                ]
            )
        else:
            line_bot_api.push_message(user_id, TextSendMessage(text="❌ 沒有符合的物件，請調整條件"))

        return jsonify({"status": "success"})

    except Exception as e:
        log.exception(f"[submit_search] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# -------------------- 啟動 --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
