@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()

    if msg == "你是誰":
        flex_card = {
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
                        "url": "https://res.cloudinary.com/daj9nkjd1/image/upload/v1753039495/%E5%A4%A7%E5%BD%AC%E7%9C%8B%E6%88%BF_%E9%A0%AD%E8%B2%BC_%E5%B7%A5%E4%BD%9C%E5%8D%80%E5%9F%9F_1_addzrg.jpg"
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
                                "offsetBottom": "10px",
                                "size": "20px"
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
                                                "color": "#7B7B7B"
                                            }
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
                                            {
                                                "type": "text",
                                                "text": "優質資深房仲",
                                                "color": "#7B7B7B"
                                            }
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
                                "text": "桃園市中壢區",
                                "size": "20px",
                                "weight": "bold",
                                "color": "#FF8000",
                                "margin": "10px"
                            },
                            {
                                "type": "text",
                                "text": "擁有多年的房地產經驗\n平時也經營 TikTok、YouTube   用影片分析房市趨勢，也分享生活趣事\n\n想買房、換屋，或了解市場，都歡迎與我聊聊！",
                                "size": "15px",
                                "wrap": True,
                                "margin": "10px"
                            },
                            {
                                "type": "separator",
                                "color": "#101010",
                                "margin": "15px"
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
                                                "text": "用影片更認識我",
                                                "color": "#ffffff"
                                            }
                                        ],
                                        "height": "30px",
                                        "maxWidth": "69%",
                                        "backgroundColor": "#FF8000",
                                        "cornerRadius": "5px",
                                        "justifyContent": "center",
                                        "alignItems": "center"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": "通話",
                                                "color": "#ffffff"
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
                                            "uri": "tel:0918837739"
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

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="自我介紹", contents=flex_card)
        )

    elif msg == "找好屋":
        houses = query_houses("agent001")
        if houses:
            flex = build_flex_message(houses[0])
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text="推薦物件", contents=flex)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="目前無推薦物件，歡迎留言需求！")
            )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入『找好屋』或『你是誰』")
        )
