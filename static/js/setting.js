// setting.js
// 功能：送出追蹤條件表單 → /submit_form → 後端 push Flex 卡片

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await liff.init({ liffId: "2007821360-8WJy7BmM" });
    const profile = await liff.getProfile();
    document.getElementById("user_id").value = profile.userId;

    document.getElementById("settingForm").addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        user_id: document.getElementById("user_id").value,
        budget: document.getElementById("budget").value,
        room: document.getElementById("room").value,
        genre: document.getElementById("genre").value,
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
