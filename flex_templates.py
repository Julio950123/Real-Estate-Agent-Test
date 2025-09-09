# flex_templates.py
"""
集中管理 Flex Message 模板
"""

from typing import Dict, Any


def buyer_card(liff_url: str) -> Dict[str, Any]:
    return {
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
                    "action": {"type": "uri", "label": "設定訂閱條件", "uri": liff_url},
                }
            ],
        },
    }


def seller_text() -> str:
    return "好的，請留下您的姓名及電話\n我將盡速與您聯繫"


from typing import Dict, Any

from typing import Dict, Any

def manage_condition_card(budget: str, room: str, genre: str, liff_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "當前追蹤條件",
                    "weight": "bold",
                    "size": "md",
                    "color": "#333333"
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "spacing": "md",
                    "contents": [
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "sm", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "sm", "wrap": True}
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
                    "action": {
                        "type": "uri",
                        "label": "更改追蹤條件",
                        "uri": liff_url
                    }
                }
            ]
        }
    }

def search_card() -> dict:
    return{
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
        "backgroundColor": "#209E72",
        "cornerRadius": "5px",
        "spacing": "xs"
      }
    ],
    "spacing": "xs"
  }
}

def intro_card() -> dict:
    return {
        "type": "carousel",
        "contents": [
            {
                "type": "bubble",
                "size": "mega",
                "hero": {
                    "type": "image",
                    "size": "80%",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "margin": "none",
                    "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1757148957/%E9%A0%AD%E8%B2%BC_a1gz5t.png"
                },
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
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "tel:0937339406"
                                    }
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

def listing_card(data: dict) -> dict:
    """單筆物件卡片"""
    image_url = data.get("image_url") or "https://picsum.photos/800/520?random=1"
    detail_url = data.get("detail_url") or "https://example.com"
    map_url = data.get("map_url") or "https://www.google.com/maps"

    return {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {"type": "uri", "uri": detail_url}
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
                            "size": "15px",
                            "flex": 8
                        },
                        {
                            "type": "text",
                            "text": data.get("address", "-"),
                            "flex": 90,
                            "color": "#7B7B7B"
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": data.get("title", "-"),
                    "weight": "bold",
                    "size": "20px"
                },
                {
                    "type": "text",
                    "text": f"{data.get('square_meters', '-') }坪｜{data.get('genre','-')}",
                    "size": "18px",
                    "margin": "5px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": data.get("detail1", ""), "align": "center", "color": "#7B7B7B"}
                            ],
                            "backgroundColor": "#e7e8e7",
                            "cornerRadius": "5px"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": data.get("detail2", ""), "align": "center", "color": "#7B7B7B"}
                            ],
                            "backgroundColor": "#e7e8e7",
                            "cornerRadius": "5px"
                        }
                    ],
                    "spacing": "md",
                    "margin": "5px"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": "（含車位價格）",
                            "size": "15px",
                            "weight": "bold",
                            "color": "#7B7B7B",
                            "align": "end",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": f"{data.get('price', 0)}萬",
                            "size": "30px",
                            "weight": "bold",
                            "color": "#FF5809",
                            "align": "end"
                        }
                    ]
                },
                {"type": "separator", "margin": "5px"}
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {"type": "uri", "label": "物件詳情", "uri": detail_url},
                            "flex": 50,
                            "color": "#EE9226",
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "action": {"type": "uri", "label": "分享", "uri": map_url},
                            "flex": 25,
                            "color": "#9D9D9D",
                            "style": "primary"
                        }
                    ]
                },
                {"type": "text", "text": "物件以現場與權狀為主", "align": "center", "size": "13px"}
            ]
        }
    }


def listings_to_carousel(listings: list) -> dict:
    """把多筆 listings 包成 carousel"""
    return {
        "type": "carousel",
        "contents": [listing_card(item) for item in listings]
    }


__all__ = [
    "buyer_card",
    "seller_text",
    "manage_condition_card",
    "intro_card",
    "listing_card",
    "search_card",
]