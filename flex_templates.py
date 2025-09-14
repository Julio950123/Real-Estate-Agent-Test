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
                {"type": "text", "text": "好的", "weight": "bold", "size": "lg"},
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
                    "color": "#EB941E",
                    "height": "sm",
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
                    "size": "lg",
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
                        {"type": "text", "text": f"預算：{budget or '-'}", "size": "lg", "wrap": True},
                        {"type": "text", "text": f"格局：{room or '-'}", "size": "lg", "wrap": True},
                        {"type": "text", "text": f"類型：{genre or '-'}", "size": "lg", "wrap": True}
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
        "backgroundColor": "#EB941E",
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

def safe_str(value, default="-"):
    """確保 Flex 的 text 一定是字串"""
    return str(value) if value not in [None, ""] else default


def listing_card(doc_id: str, data: dict) -> dict:
    """單筆物件卡片"""
    image_url = safe_str(data.get("image_url"), "https://picsum.photos/800/520?random=1")

    return {
        "type": "bubble",
        "size": "mega",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
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
                            "text": safe_str(data.get("address")),
                            "flex": 90,
                            "color": "#7B7B7B",
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": safe_str(data.get("title")),
                    "weight": "bold",
                    "size": "20px"
                },
                {
                    "type": "text",
                    "text": f"{safe_str(data.get('square_meters'))}坪｜{safe_str(data.get('genre'))}",
                    "size": "18px",
                    "color": "#555555",
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
                                {
                                    "type": "text",
                                    "text": safe_str(data.get("detail1")),
                                    "align": "center",
                                    "color": "#7B7B7B",
                                }
                            ],
                            "backgroundColor": "#e7e8e7",
                            "cornerRadius": "5px"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": safe_str(data.get("detail2")),
                                    "align": "center",
                                    "color": "#7B7B7B",
                                }
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
                            "gravity": "bottom",
                            "offsetBottom": "5px"
                        },
                        {
                            "type": "text",
                            "text": f"{safe_str(data.get('price'), 0)}萬",
                            "size": "30px",
                            "weight": "bold",
                            "color": "#FF5809",
                            "margin": "5px",
                            "align": "end",
                            "flex": 0
                        }
                    ],
                    "margin": "5px",
                    "offsetTop": "5px"
                },
                {"type": "separator", "margin": "5px"},
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                            "type": "button",
                            "height": "sm",
                            "flex": 50,
                            "color": "#EE9226",
                            "style": "primary",
                            "action": {
                                "type": "postback",
                                "label": "物件詳情",
                                "data": f"action=detail&id={doc_id}"
                            }
                        },
                        {
                            "type": "button",
                            "height": "sm",
                            "flex": 25,
                            "color": "#9D9D9D",
                            "style": "primary",
                            "action": {
                                "type": "uri",
                                "label": "分享",
                                "uri": f"https://liff.line.me/2007821360-5zM287yq?doc_id={doc_id}"
                            }
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": "物件以現場與權狀為主",
                    "align": "center",
                    "size": "13px",
                }
            ],
            "spacing": "md",
            "offsetTop": "13px"
        }
    }


def listings_to_carousel(listings: list) -> dict:
    """把多筆 listings 包成 carousel"""
    return {
        "type": "carousel",
        "contents": [
            listing_card(item.get("id", "noid"), item) for item in listings
        ]
    }


def property_flex(doc_id: str, data: dict) -> dict:
    """回傳物件詳情的 Flex Message (三個 bubble)"""

    return {
        "type": "carousel",
        "contents": [

            # ----------------- Bubble 1：封面卡 -----------------
            {
                "type": "bubble",
                "size": "mega",
                "hero": {
                    "type": "image",
                    "url": data.get("image_url", "https://picsum.photos/800/520"),
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [

                        # 地址
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

                        # 標題
                        {
                            "type": "text",
                            "text": data.get("title", "未命名物件"),
                            "weight": "bold",
                            "size": "20px"
                        },

                        # 坪數 + 類型
                        {
                            "type": "text",
                            "text": f'{data.get("square_meters", "?")}坪｜{data.get("genre", "-")}',
                            "size": "18px",
                            "margin": "5px"
                        },

                        # 標籤 (detail1, detail2)
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("detail1", ""),
                                            "align": "center",
                                            "color": "#7B7B7B"
                                        }
                                    ],
                                    "backgroundColor": "#e7e8e7",
                                    "cornerRadius": "5px"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("detail2", ""),
                                            "align": "center",
                                            "color": "#7B7B7B"
                                        }
                                    ],
                                    "backgroundColor": "#e7e8e7",
                                    "cornerRadius": "5px"
                                }
                            ],
                            "spacing": "md",
                            "margin": "5px"
                        },

                        # 價格
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
                                    "align": "end"
                                },
                                {
                                    "type": "text",
                                    "text": f'{data.get("price", "?")} 萬',
                                    "size": "30px",
                                    "weight": "bold",
                                    "color": "#FF5809",
                                    "align": "end",
                                    "flex": 0
                                }
                            ],
                            "margin": "5px"
                        },

                        {"type": "separator", "margin": "5px"},

                        # 按鈕：預約賞屋
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "預約賞屋",
                                "uri": "http://linecorp.com/"
                            },
                            "color": "#EE9226",
                            "style": "primary",
                            "margin": "md",
                            "height": "sm"
                        },

                        # 備註
                        {
                            "type": "text",
                            "text": "物件以現場與權狀為主",
                            "align": "center",
                            "size": "13px",
                            "margin": "md"
                        }
                    ]
                }
            },

            # ----------------- Bubble 2：格局卡 -----------------
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [

                        # 標題 + 獨家專任
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": data.get("project_name", ""),
                                    "size": "30px",
                                    "flex": 0
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("exclusive", ""),
                                            "color": "#307B91"
                                        }
                                    ],
                                    "cornerRadius": "5px",
                                    "borderColor": "#307B91",
                                    "borderWidth": "1px",
                                    "alignItems": "center",
                                    "flex": 0
                                }
                            ],
                            "spacing": "lg",
                            "alignItems": "center"
                        },

                        {"type": "separator", "color": "#165161", "margin": "md"},

                        # 格局
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "格局", "color": "#8A8F91", "flex": 0},
                                {"type": "text", "text": data.get("pattern", "")}
                            ],
                            "margin": "md",
                            "spacing": "xl"
                        },

                        # 屋齡 + 樓高
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "屋齡", "color": "#8A8F91", "flex": 0},
                                {"type": "text", "text": data.get("old", ""), "flex": 0},
                                {"type": "text", "text": "樓高", "color": "#8A8F91", "flex": 0},
                                {"type": "text", "text": data.get("height", "")}
                            ],
                            "margin": "md",
                            "spacing": "xl"
                        },

                        # 坪數
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {"type": "text", "text": "權狀坪數", "color": "#8A8F91", "flex": 0},
                                {"type": "text", "text": f'{data.get("square_meters2", "")} 坪 (不含車位)'}
                            ],
                            "margin": "md",
                            "spacing": "xl"
                        },

                        # 格局圖
                        {
                            "type": "image",
                            "url": data.get("pattern_url", "https://picsum.photos/800/520"),
                            "size": "full"
                        },

                        # 影片 + 導航
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "用影片看更多",
                                        "uri": data.get("video_uri", "http://linecorp.com/")
                                    },
                                    "color": "#EE9226",
                                    "style": "primary",
                                    "flex": 50,
                                    "height": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                        "type": "uri",
                                        "label": "導航",
                                        "uri": data.get("map_uri", "http://maps.google.com/")
                                    },
                                    "color": "#9D9D9D",
                                    "style": "primary",
                                    "flex": 25,
                                    "height": "sm"
                                }
                            ],
                            "spacing": "md"
                        }
                    ]
                }
            },

            # ----------------- Bubble 3：完整文案 -----------------
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": data.get("text", ""),
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }



__all__ = [
    "buyer_card",
    "seller_text",
    "manage_condition_card",
    "intro_card",
    "listing_card",
    "search_card",
    "listings_to_carousel",  
]