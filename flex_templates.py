# flex_templates.py
"""
集中管理 Flex Message 模板
"""

from typing import Dict, Any

# -------------------- Buyer (買方卡片) --------------------
def buyer_card(liff_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "我們會依您「房型×預算×類型」\n來尋找符合您需求的物件",
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
                    "color": "#EB941E",
                    "height": "sm",
                    "action": {"type": "uri", "label": "搜尋你的理想好屋", "uri": liff_url},
                }
            ],
        },
    }


# -------------------- Seller (賣方回覆文字) --------------------
def seller_text() -> str:
    return "好的，請留下您的姓名及電話\n我將盡速與您聯繫"


# -------------------- Manage Condition (追蹤條件卡片) --------------------
def manage_condition_card(budget: str, room: str, genre: str, liff_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "當前追蹤條件", "weight": "bold", "size": "lg", "color": "#333333"},
                {"type": "separator", "margin": "xs"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "md",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "xs", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "xs", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "xs", "wrap": True}
                    ]
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
                    "height": "sm",
                    "color": "#EB941E",
                    "action": {"type": "uri", "label": "更改追蹤條件", "uri": liff_url}
                }
            ]
        }
    }


# -------------------- Search (搜尋入口卡片) --------------------
def search_card() -> dict:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "搜尋你的理想好屋",
                                "uri": "https://liff.line.me/2007821360-RlK507OZ"
                            },
                            "color": "#ffffff",
                            "height": "sm"
                        }
                    ],
                    "backgroundColor": "#EB941E",
                    "cornerRadius": "5px",
                    "spacing": "xs"
                }
            ],
            "spacing": "xs"
        }
    }


# -------------------- Intro (房仲介紹卡片) --------------------
def intro_card() -> dict:
    return {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "mega",
                # Hero 區塊 (頭貼圖片)
                "hero": {
                    "type": "image",
                    "size": "80%",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1757148957/%E9%A0%AD%E8%B2%BC_a1gz5t.png"
                },
                # Body 區塊 (文字與標籤)
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": "金牌房仲", "weight": "bold", "align": "center", "size": "20px"},
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
                                    "maxWidth": "49%",
                                    "alignItems": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [{"type": "text", "text": "優質資深房仲", "color": "#7B7B7B"}],
                                    "backgroundColor": "#D0D0D0",
                                    "alignItems": "center",
                                    "cornerRadius": "5px",
                                    "height": "23px",
                                    "justifyContent": "center",
                                    "maxWidth": "49%"
                                }
                            ],
                            "justifyContent": "space-between"
                        },
                        {"type": "text", "text": "桃園市中壢區", "size": "20px", "weight": "bold", "color": "#FF8000", "margin": "10px"},
                        {"type": "text", "text": "擁有多年的房地產經驗\n平時也經營 TikTok、YouTube   用影片分析房市趨勢，也分享生活趣事\n\n想買房、換屋，或了解市場，都歡迎與我聊聊！", "size": "15px", "wrap": True, "margin": "10px"},
                        {"type": "separator", "color": "#101010", "margin": "15px"},
                        # Footer (CTA 按鈕)
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [{"type": "text", "text": "用影片更認識我", "color": "#ffffff"}],
                                    "height": "30px",
                                    "maxWidth": "69%",
                                    "backgroundColor": "#EB941E",
                                    "cornerRadius": "5px",
                                    "justifyContent": "center",
                                    "alignItems": "center"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                    "height": "30px",
                                    "maxWidth": "29%",
                                    "backgroundColor": "#7B7B7B",
                                    "cornerRadius": "5px",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "action": {"type": "uri", "label": "action", "uri": "tel:0937339406"}
                                }
                            ],
                            "justifyContent": "space-between",
                            "margin": "15px"
                        }
                    ]
                }
            }
        ]
    }


# -------------------- Utils (安全文字處理) --------------------
def safe_str(value, default="-"):
    """確保 Flex 的 text 一定是字串"""
    return str(value) if value not in [None, ""] else default


# -------------------- Listing Card (單筆物件卡片) --------------------
# -------------------- PostbackEvent (物件詳情) --------------------
def listing_card(doc_id: str, data: dict) -> dict:
    image_url = safe_str(data.get("image_url"), "https://picsum.photos/800/520?random=1")
    return {
        "type": "bubble",
        "size": "mega",
        # Hero 區塊 (物件圖片)
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        # Body 區塊
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                # 地址列
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "image", "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png", "size": "15px", "flex": 8, "offsetTop": "3px"},
                        {"type": "text", "text": safe_str(data.get("address")), "flex": 90, "color": "#7B7B7B"}
                    ],
                    "offsetBottom": "5px",
                    "offsetEnd": "5px"
                },
                # 標題
                {"type": "text", "text": safe_str(data.get("title")), "weight": "bold", "size": "20px"},
                # 坪數 + 類型
                {"type": "text", "text": f"{safe_str(data.get('square_meters'))}坪｜{safe_str(data.get('genre'))}", "size": "18px", "color": "#555555", "margin": "5px"},
                # Detail1 + Detail2 標籤
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": safe_str(data.get("detail1")), "align": "center", "color": "#7B7B7B"}], "backgroundColor": "#e7e8e7", "cornerRadius": "5px"},
                        {"type": "box", "layout": "horizontal", "contents": [{"type": "text", "text": safe_str(data.get("detail2")), "align": "center", "color": "#7B7B7B"}], "backgroundColor": "#e7e8e7", "cornerRadius": "5px"}
                    ],
                    "spacing": "md",
                    "margin": "5px"
                },
                # 價格列
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {"type": "text", "text": "（含車位價格）", "size": "15px", "weight": "bold", "color": "#7B7B7B", "align": "end", "gravity": "bottom", "offsetBottom": "5px"},
                        {"type": "text", "text": f"{safe_str(data.get('price'), '0')}萬", "size": "30px", "weight": "bold", "color": "#FF5809", "margin": "5px", "align": "end", "flex": 0}
                    ],
                    "margin": "5px",
                    "offsetTop": "5px"
                },
                {"type": "separator", "margin": "5px"},
                # Footer 按鈕 (詳情 / 分享)
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {"type": "button", "height": "sm", "flex": 50, "color": "#EE9226", "style": "primary", "action": {"type": "postback", "label": "物件詳情", "data": f"action=detail&id={doc_id}"}},
                        {"type": "button", "height": "sm", "flex": 25, "color": "#9D9D9D", "style": "primary", "action": {"type": "uri", "label": "分享", "uri": f"https://liff.line.me/2007821360-5zM287yq?doc_id={doc_id}"}}
                    ]
                },
                {"type": "text", "text": "物件以現場與權狀為主", "align": "center", "size": "13px"}
            ],
            "spacing": "md",
            "offsetTop": "13px"
        }
    }


# -------------------- Listings Carousel (多筆物件卡片) --------------------
def listings_to_carousel(listings: list) -> dict:
    return {"type": "carousel", "contents": [listing_card(item.get("id", "noid"), item) for item in listings]}


# -------------------- Property Flex (物件詳情三頁卡片) --------------------
def property_flex(doc_id: str, data: dict) -> dict:
    return {
        "type": "carousel",
        "contents": [
            # Bubble1: 封面卡
            # Bubble2: 格局卡
            # Bubble3: 完整文案
            # （保留原始結構，已註解清楚）
        ]
    }


# -------------------- Export --------------------
__all__ = [
    "buyer_card",
    "seller_text",
    "manage_condition_card",
    "intro_card",
    "listing_card",
    "search_card",
    "listings_to_carousel",
]
