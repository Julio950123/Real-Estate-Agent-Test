from flex_templates import listings_to_carousel

@app.route("/submit_search", methods=["POST"])
def submit_search():
    try:
        data = extract_form_data()
        log.info(f"[submit_search] 收到資料: {data}")

        budget = data.get("budget")
        room   = data.get("room")
        genre  = data.get("genre")
        user_id = data.get("user_id")

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
        except ValueError:
            log.warning(f"[submit_search] 預算格式錯誤: {budget}")

        # 🔎 格局條件
        try:
            if room and room not in ["不限", "0"]:
                query = query.where("room", "==", int(room))
        except ValueError:
            log.warning(f"[submit_search] 格局格式錯誤: {room}")

        # 🔎 類型條件
        if genre and genre != "不限":
            query = query.where("genre", "==", genre)

        docs = query.limit(5).stream()
        listings = [doc.to_dict() for doc in docs]
        log.info(f"[submit_search] 找到 {len(listings)} 筆 listings")

        # 回傳 LINE 訊息
        if listings:
            # 多筆 → Carousel
            carousel = listings_to_carousel(listings)

            line_bot_api.push_message(
                user_id,
                [
                    TextSendMessage(text="您想要的理想好屋條件為…\n正在為您搜尋中 🔍"),
                    FlexSendMessage(alt_text="找到物件", contents=carousel)
                ]
            )
        else:
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="❌ 沒有符合的物件，請調整條件")
            )

        return jsonify({"status": "success"})

    except Exception as e:
        log.exception(f"[submit_search] error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500