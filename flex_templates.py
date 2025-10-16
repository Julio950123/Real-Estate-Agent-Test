# flex_templates.py
"""
集中管理 Flex Message 模板
"""

from typing import Dict, Any

# -------------------- no_result_flex (沒有符合條件的物件) --------------------
def no_result_card(liff_url: str) -> Dict[str, Any]:
    """
    回傳『沒有符合條件的物件』提示卡。
    可傳入任何 LIFF 表單連結，用於買屋、租屋或預約等情境。
    """
    return {
        "type": "bubble",
        "size": "mega",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "沒有符合條件的物件",
                            "size": "lg",
                            "color": "#101010"
                        },
                        {
                            "type": "text",
                            "text": "可以填寫需求表單 📋\n當有符合的物件時第一時間通知您！",
                            "wrap": True,
                            "size": "sm",
                            "color": "#666666",
                            "margin": "md"
                        }
                    ]
                },
                {
                    "type": "button",
                    "action": {
                        "type": "uri",
                        "label": "填寫需求表單",
                        "uri": "https://liff.line.me/2007720984-AYJY7nWQ"
                    },
                    "style": "primary",
                    "color": "#EB941E",
                    "margin": "lg",
                    "height": "sm"
                }
            ]
        },
        "styles": {
            "body": {"backgroundColor": "#FFFFFF"}
        }
    }


# -------------------- Buyer (我的追蹤條件卡片) --------------------
def buyer_card(liff_url: str) -> Dict[str, Any]:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "我們會依您「房型×預算×類型」\n在未來有符合您需求的物件時\n第一時間通知您",
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
                    "action": {"type": "uri", "label": "設定追蹤條件", "uri": "https://liff.line.me/2007821360-8WJy7BmM"},
                }
            ],
        },
    }


# -------------------- Seller (賣方回覆文字) --------------------
def seller_card() -> dict:
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "了解～我可以先幫你估個合理行情！\n這樣你能知道目前大約能賣多少 ",
                    "wrap": True,
                    "size": "md",
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
                    "color": "#EB941E",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "幫我評估行情",
                        "uri": "https://liff.line.me/【你的LIFF_ID】?form=entrust"
                    }
                }
            ]
        }
    }


# -------------------- Manage Condition (追蹤條件卡片) --------------------
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
                    "size": "sm",
                    "color": "#333333",
                    "margin": "sm"
                },
                {"type": "separator", "margin": "xs"},
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
                    "action": {"type": "uri", "label": "更改追蹤條件", "uri": "https://liff.line.me/2007821360-8WJy7BmM"}
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
            # ---------- Bubble 1：房仲介紹 ----------
            {
                "type": "bubble",
                "size": "mega",
                "hero": {
                    "type": "image",
                    "size": "80%",
                    "aspectMode": "cover",
                    "aspectRatio": "1:1",
                    "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1759426766/%E9%A0%AD%E8%B2%BC1_d3e46l.png"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "彭俊偉",
                            "weight": "bold",
                            "align": "center",
                            "size": "20px",
                            "offsetBottom": "20px"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {"type": "text", "text": "11年資深房仲", "color": "#7B7B7B"}
                                    ],
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
                                    "contents": [
                                        {"type": "text", "text": "飛躍團隊", "color": "#7B7B7B"}
                                    ],
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
                        {
                            "type": "text",
                            "text": "南北桃五店連線",
                            "size": "20px",
                            "weight": "bold",
                            "color": "#FF8000",
                            "margin": "10px"
                        },
                        {
                            "type": "text",
                            "text": "多年成交與團隊實戰經驗，專精：\n📍 不動產買賣委託\n📍 房價估價 / 稅務規劃\n📍 市場趨勢諮詢\n想要買房、賣屋、換屋或了解市場，\n都歡迎與我聊聊！",
                            "size": "15px",
                            "wrap": True,
                            "margin": "10px"
                        },
                        {"type": "separator", "color": "#101010", "margin": "15px"},
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {"type": "text", "text": "用影片更認識我", "color": "#ffffff"}
                                    ],
                                    "height": "30px",
                                    "maxWidth": "69%",
                                    "backgroundColor": "#EB941E",
                                    "cornerRadius": "5px",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "https://www.instagram.com/junwei801226/"
                                    }
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {"type": "text", "text": "通話", "color": "#ffffff"}
                                    ],
                                    "height": "30px",
                                    "maxWidth": "29%",
                                    "backgroundColor": "#7B7B7B",
                                    "cornerRadius": "5px",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                    "action": {
                                        "type": "uri",
                                        "label": "action",
                                        "uri": "tel:0930728018"
                                    }
                                }
                            ],
                            "justifyContent": "space-between",
                            "margin": "15px"
                        }
                    ]
                }
            },

            # ---------- Bubble 2：南北桃五店 ----------
            {
                "type": "bubble",
                "size": "mega",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        # 店1
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "21世紀 海華SOGO店", "weight": "bold", "size": "18px"},
                                {"type": "text", "text": "桃園市中壢區環北路319號", "size": "15px", "color": "#BABABA"},
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "地圖引導", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "69%",
                                            "backgroundColor": "#425663",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://maps.app.goo.gl/ZE93s7DR8zyDZoUn6"
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "29%",
                                            "backgroundColor": "#A3A3A3",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:034514599"
                                            }
                                        }
                                    ],
                                    "justifyContent": "space-between",
                                    "margin": "15px",
                                    "offsetBottom": "10px"
                                }
                            ]
                        },
                        {"type": "separator", "color": "#101010", "margin": "2px"},
                        # 店2
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "中信房屋 中壢站前店", "weight": "bold", "size": "18px"},
                                {"type": "text", "text": "桃園市中壢區中北路二段79號", "size": "15px", "color": "#BABABA"},
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "地圖引導", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "69%",
                                            "backgroundColor": "#425663",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://maps.app.goo.gl/niHKxQfw42vVKMPu6"
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "29%",
                                            "backgroundColor": "#A3A3A3",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:034591013"
                                            }
                                        }
                                    ],
                                    "justifyContent": "space-between",
                                    "margin": "15px",
                                    "offsetBottom": "10px"
                                }
                            ],
                            "offsetTop": "10px"
                        },
                        {"type": "separator", "color": "#101010", "margin": "10px"},
                        # 店3
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "中信房屋 中壢體育園區加盟店", "weight": "bold", "size": "18px"},
                                {"type": "text", "text": "桃園市中壢區中山東路二段542號", "size": "15px", "color": "#BABABA"},
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "地圖引導", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "69%",
                                            "backgroundColor": "#425663",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://maps.app.goo.gl/4NzN4Zr5TBVNjV9J9"
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "29%",
                                            "backgroundColor": "#A3A3A3",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:034161888"
                                            }
                                        }
                                    ],
                                    "justifyContent": "space-between",
                                    "margin": "15px",
                                    "offsetBottom": "10px"
                                }
                            ],
                            "offsetTop": "10px"
                        },
                        {"type": "separator", "color": "#101010", "margin": "10px"},
                        # 店4
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "太平洋房屋 桃園永安加盟店", "weight": "bold", "size": "18px"},
                                {"type": "text", "text": "桃園市桃園區永安路285號", "size": "15px", "color": "#BABABA"},
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "地圖引導", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "69%",
                                            "backgroundColor": "#425663",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://maps.app.goo.gl/2Mm9vfGNxrSwjH2a7"
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "29%",
                                            "backgroundColor": "#A3A3A3",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:033397999"
                                            }
                                        }
                                    ],
                                    "justifyContent": "space-between",
                                    "margin": "15px",
                                    "offsetBottom": "10px"
                                }
                            ],
                            "offsetTop": "10px"
                        },
                        {"type": "separator", "color": "#101010", "margin": "10px"},
                        # 店5
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {"type": "text", "text": "21世紀 桃園藝文店", "weight": "bold", "size": "18px"},
                                {"type": "text", "text": "桃園市桃園區經國路336巷2號", "size": "15px", "color": "#BABABA"},
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "地圖引導", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "69%",
                                            "backgroundColor": "#425663",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://maps.app.goo.gl/H7NjgFJa7ovmmtjXA"
                                            }
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [{"type": "text", "text": "通話", "color": "#ffffff"}],
                                            "height": "30px",
                                            "maxWidth": "29%",
                                            "backgroundColor": "#A3A3A3",
                                            "cornerRadius": "5px",
                                            "justifyContent": "center",
                                            "alignItems": "center",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:033580318"
                                            }
                                        }
                                    ],
                                    "justifyContent": "space-between",
                                    "margin": "15px",
                                    "offsetBottom": "10px"
                                }
                            ],
                            "offsetTop": "10px"
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
def listing_card(doc_id: str, data: dict) -> dict:
    image_url = safe_str(
        data.get("image_url"),
        "https://picsum.photos/800/520?random=1"
    )
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
            "spacing": "md",
            "offsetTop": "0px",
            "contents": [

                # 地址列
                {
                    "type": "box",
                    "layout": "horizontal",
                    "offsetEnd": "5px",
                    "contents": [
                        {
                            "type": "image",
                            "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
                            "size": "15px",
                            "flex": 8,
                            "offsetTop": "3px"
                        },
                        {
                            "type": "text",
                            "text": safe_str(data.get("address")),
                            "flex": 90,
                            "color": "#7B7B7B"
                        }
                    ]
                },

                # 標題
                {
                    "type": "text",
                    "text": safe_str(data.get("title")),
                    "weight": "bold",
                    "size": "25px",
                    "offsetBottom": "2px"
                },

                # 坪數 + 類型
                {
                    "type": "text",
                    "text": f"{safe_str(data.get('square_meters'))}坪｜{safe_str(data.get('genre'))}",
                    "size": "18px",
                    "color": "#555555",
                    "margin": "5px",
                    "offsetBottom": "2px"
                },

                # Detail1 + Detail2 標籤
                {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "margin": "5px",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "cornerRadius": "5px",
                            "backgroundColor": "#e7e8e7",
                            "height": "30px",
                            "alignItems": "center",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": safe_str(data.get("detail1")),
                                    "align": "center",
                                    "color": "#7B7B7B"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "cornerRadius": "5px",
                            "backgroundColor": "#e7e8e7",
                            "height": "30px",
                            "alignItems": "center",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": safe_str(data.get("detail2")),
                                    "align": "center",
                                    "color": "#7B7B7B"
                                }
                            ]
                        }
                    ]
                },

                # 價格列
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "5px",
                    "offsetTop": "5px",
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
                            "text": f"{safe_str(data.get('price'), '0')}萬",
                            "size": "30px",
                            "weight": "bold",
                            "color": "#FF5809",
                            "margin": "5px",
                            "align": "end",
                            "flex": 0
                        }
                    ]
                },

                {
                    "type": "separator",
                    "margin": "5px"
                },

                # Footer 按鈕 (詳情 / 分享)
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

                # 備註文字
                {
                    "type": "text",
                    "text": "物件以現場與權狀為主",
                    "align": "center",
                    "size": "13px",
                    "color": "#7B7B7B",
                    "offsetTop": "3px"
                }
            ]
        }
    }


# -------------------- Listings Carousel (多頁物件卡片) --------------------
import urllib.parse
def normalize_text(raw: str) -> str:
    if not raw:
        return ""
    return raw.replace("\\n\\n", "\n\n").replace("\\n", "\n").strip()

def safe_str(val, default=""):
    if val is None:
        return default
    return str(val)

def property_flex(doc_id: str, data: dict) -> dict:
    """回傳物件詳情的 Flex Message (三個 bubble)"""

    # 固定 booking LIFF URL
    LIFF_URL_BOOKING = "https://liff.line.me/2007821360-g5ploEDy"

    # 格式化文字
    text = normalize_text(data.get("text", ""))

    # 組合 booking_url（帶 id & title）
    title = data.get("title", "")
    title_encoded = urllib.parse.quote(title)
    booking_url = f"{LIFF_URL_BOOKING}?id={doc_id}&title={title_encoded}"


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
                    "spacing": "md",
                    "offsetTop": "0px",
                    "contents": [

                        # 地址
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "offsetEnd": "5px",
                            "contents": [
                                {
                                    "type": "image",
                                    "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
                                    "size": "15px",
                                    "flex": 8,
                                    "offsetTop": "3px"
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
                            "size": "25px",
                            "offsetBottom": "2px"
                        },

                        # 坪數 + 類型
                        {
                            "type": "text",
                            "text": f'{data.get("square_meters", "?")}坪｜{data.get("genre", "-")}',
                            "size": "18px",
                            "margin": "5px",
                            "offsetBottom": "2px"
                        },

                        # 標籤 (detail1, detail2)
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "spacing": "md",
                            "margin": "5px",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "cornerRadius": "5px",
                                    "backgroundColor": "#e7e8e7",
                                    "height": "30px",
                                    "alignItems": "center",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("detail1", ""),
                                            "align": "center",
                                            "color": "#7B7B7B"
                                        }
                                    ]
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "cornerRadius": "5px",
                                    "backgroundColor": "#e7e8e7",
                                    "height": "30px",
                                    "alignItems": "center",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("detail2", ""),
                                            "align": "center",
                                            "color": "#7B7B7B"
                                        }
                                    ]
                                }
                            ]
                        },

                        # 價格
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "5px",
                            "offsetTop": "5px",
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
                                    "text": f"{safe_str(data.get('price'), '0')}萬",
                                    "size": "30px",
                                    "weight": "bold",
                                    "color": "#FF5809",
                                    "margin": "5px",
                                    "align": "end",
                                    "flex": 0
                                }
                            ]
                        },

                        {
                            "type": "separator",
                            "margin": "5px"
                        }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "button",
                            "action": {
                                "type": "uri",
                                "label": "預約賞屋",
                                "uri": booking_url
                            },
                            "color": "#EE9226",
                            "style": "primary",
                            "margin": "md",
                            "height": "sm"
                        },
                        {
                            "type": "text",
                            "text": "物件以現場與權狀為主",
                            "align": "center",
                            "size": "13px",
                            "color": "#7B7B7B",
                            "margin": "sm",
                            "offsetTop": "3px"
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
                            "spacing": "lg",
                            "alignItems": "center",
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
                                    "cornerRadius": "5px",
                                    "borderColor": "#307B91",
                                    "borderWidth": "1px",
                                    "alignItems": "center",
                                    "flex": 0,
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": data.get("exclusive", ""),
                                            "color": "#307B91"
                                        }
                                    ]
                                }
                            ]
                        },

                        {
                            "type": "separator",
                            "color": "#165161",
                            "margin": "md"
                        },

                        # 格局
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "spacing": "xl",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "格局",
                                    "color": "#8A8F91",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": data.get("pattern", "")
                                }
                            ]
                        },

                        # 屋齡 + 樓高
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "spacing": "xl",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "屋齡",
                                    "color": "#8A8F91",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": data.get("old", ""),
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "樓高",
                                    "color": "#8A8F91",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": data.get("height", "")
                                }
                            ]
                        },

                        # 坪數
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "spacing": "xl",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "權狀坪數",
                                    "color": "#8A8F91",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": f'{data.get("square_meters2", "")} (不含車位)'
                                }
                            ]
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
                            "spacing": "md",
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
                            ]
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
                            "text": text,   # ✅ 使用處理過的文字
                            "wrap": True
                        }
                    ]
                }
            }
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

