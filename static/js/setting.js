// setting.js
// 功能：送出追蹤條件表單 → /submit_form → 後端 push Flex 卡片

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await liff.init({ liffId: "2007821360-8WJy7BmM" }); // ⚠️ 記得換成你的 LIFF ID
    const profile = await liff.getProfile();
    document.getElementById("user_id").value = profile.userId;

    // 👇 新增：型態變化時控制格局欄位顯示/隱藏
    const genreSelect = document.getElementById("genre");
    const roomField = document.getElementById("roomField");
    const roomSelect = document.getElementById("room");
    const hiddenTypes = ["店面", "土地", "辦公"];

    genreSelect.addEventListener("change", () => {
      if (hiddenTypes.includes(genreSelect.value)) {
        roomField.style.display = "none";
        roomSelect.removeAttribute("required");
      } else {
        roomField.style.display = "block";
        roomSelect.setAttribute("required", "required");
      }
    });

    // 👇 表單送出
    document.getElementById("settingForm").addEventListener("submit", async (e) => {
      e.preventDefault();

      const genre = genreSelect.value;
      let roomValue = roomSelect.value;

      // 👇 若為隱藏類型，自動清空 room 值
      if (hiddenTypes.includes(genre)) {
        roomValue = "";
      }

      const data = {
        user_id: document.getElementById("user_id").value,
        budget: document.getElementById("budget").value,
        room: roomValue,
        genre: genre,
      };

      try {
        const res = await fetch("/submit_form", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        const result = await res.json();
        if (result.status === "success") {
          await liff.closeWindow(); // ✅ 後端會 push Flex 回 LINE
        } else {
          alert("❌ 送出失敗：" + result.message);
        }
      } catch (err) {
        console.error("[setting.js] error:", err);
        alert("❌ 發生錯誤，請稍後再試");
      }
    });
  } catch (err) {
    console.error("[setting.js] LIFF init error:", err);
    alert("❌ LIFF 初始化失敗");
  }
});
