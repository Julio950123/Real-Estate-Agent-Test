def buyer_card(liff_url: str):
    return {
        "type": "bubble",
        "body": {"type": "box","layout": "vertical","contents": [
            {"type": "text","text": "太好了！🎯","weight": "bold","size": "lg"},
            {"type": "text","text": "我能幫你推薦合適的房子、安排看房\n也能依你的需求推薦物件","size": "sm","wrap": True,"margin": "md"},
        ]},
        "footer": {"type": "box","layout": "vertical","contents": [
            {"type": "button","style": "primary","color": "#00C300",
             "action": {"type": "uri","label": "設定訂閱條件","uri": liff_url}}
        ]},
    }

def seller_text():
    return "📋 請前往表單填寫出售資料：\nhttps://你的網域/sell"

def manage_condition_card(liff_url: str):
    return {
        "type": "bubble","size": "micro",
        "body": {"type": "box","layout": "vertical","contents": [
            {"type": "text","text": "🔧 修改追蹤條件","weight": "bold","size": "md","color": "#333"},
            {"type": "text","text": "點擊下方按鈕即可更新你的訂閱需求","size": "sm","wrap": True,"margin": "md"},
        ]},
        "footer": {"type": "box","layout": "vertical","contents": [
            {"type": "button","style": "primary","color": "#0066FF",
             "action": {"type": "uri","label": "修改追蹤條件","uri": liff_url}}
        ]},
    }

def intro_card():
    return {
        "type": "carousel",
        "contents": [{
            "type": "bubble","size": "mega",
            "hero": {"type": "image","size": "full","aspectMode": "cover","aspectRatio": "1:1",
                     "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1753039495/%E5%A4%A7%E5%BD%AC%E7%9C%8B%E6%88%BF_%E9%A0%AD%E8%B2%BC_%E5%B7%A5%E4%BD%9C%E5%8D%80%E5%9F%9F_1_addzrg.jpg"},
            "body": {"type": "box","layout": "vertical","contents": [
                {"type": "text","text": "張大彬 Leo","weight": "bold","align": "center","size": "xl"},
                {"type": "text","text": "桃園市中壢區","size": "lg","weight": "bold","color": "#FF8000","margin": "md"},
                {"type": "text","text": "擁有多年的房地產經驗\n也經營 TikTok、YouTube 分享房市趨勢與生活趣事\n\n想買房、換屋，或了解市場，都歡迎與我聊聊！",
                 "size": "sm","wrap": True,"margin": "md"},
            ]}
        }]
    }

__all__ = ["buyer_card", "seller_text", "manage_condition_card", "intro_card"]