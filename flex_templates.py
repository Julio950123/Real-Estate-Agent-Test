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
    return "📋 請前往表單填寫出售資料：\nhttps://你的網域/sell"


def manage_condition_card(liff_url: str) -> Dict[str, Any]:
    return {
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
                    "color": "#333333",
                },
                {
                    "type": "text",
                    "text": "點擊下方按鈕即可更新你的訂閱需求",
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
                    "color": "#0066FF",
                    "action": {"type": "uri", "label": "修改追蹤條件", "uri": liff_url},
                }
            ],
        },
    }


def intro_card() -> Dict[str, Any]:
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
                    "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1753039495/%E5%A4%A7%E5%BD%AC%E7%9C%8B%E6%88%BF_%E9%A0%AD%E8%B2%BC_%E5%B7%A5%E4%BD%9C%E5%8D%80%E5%9F%9F_1_addzrg.jpg",
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "張大彬 Leo",
                            "weight": "bold",
                            "align": "center",
                            "contents": [],
                            "offsetBottom": "10px",
                            "size": "20px",
                        },
                          {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "新世代自媒體",
                                            "color": "#7B7B7B",
                                        }
                                    ],
                                    "backgroundColor": "#D0D0D0",
                                    "cornerRadius": "5px",
                                    "height": "23px",
                                    "justifyContent": "center",
                                    "maxWidth": "49%",
                                    "alignItems": "center",
                                },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "優質資深房仲",
                                            "color": "#7B7B7B",
                                        }
                                    ],
                                    "backgroundColor": "#D0D0D0",
                                    "alignItems": "center",
                                    "cornerRadius": "5px",
                                    "height": "23px",
                                    "justifyContent": "center",
                                    "maxWidth": "49%",
                                },
                            ],
                            "justifyContent": "space-between",
                        },
                          {
                            "type": "text",
                            "text": "桃園市中壢區",
                            "contents": [],
                            "size": "20px",
                            "weight": "bold",
                            "color": "#FF8000",
                            "margin": "10px",
                        },
                          {
                            "type": "text",
                            "text": "擁有多年的房地產經驗\n平時也經營 TikTok、YouTube   用影片分析房市趨勢，也分享生活趣事\n\n想買房、換屋，或了解市場，都歡迎與我聊聊！",
                            "size": "15px",
                            "wrap": true,
                            "margin": "10px",
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
                                        {
                                            "type": "text",
                                            "text": "用影片更認識我",
                                            "color": "#ffffff",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "https://www.tiktok.com/@leochang9453",
                                            },
                                        }
                                    ],
                                    "height": "30px",
                                    "maxWidth": "69%",
                                    "backgroundColor": "#FF8000",
                                    "cornerRadius": "5px",
                                    "justifyContent": "center",
                                    "alignItems": "center",
                                },
                                  {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "通話",
                                            "color": "#ffffff",
                                            "action": {
                                                "type": "uri",
                                                "label": "action",
                                                "uri": "tel:0918837739",
                                            },
                                        }
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
                                        "uri": "tel:0918837739",
                                    },
                                },
                            ],
                            "justifyContent": "space-between",
                            "margin": "15px",
                        },
                    ],
                    "position": "relative",
                    "justifyContent": "space-between",
                },
            }
        ],
    }


__all__ = ["buyer_card", "seller_text", "manage_condition_card", "intro_card"]
