// book.js
// 功能：送出預約賞屋表單 → /api/booking → 後端 push Flex 卡片

document.addEventListener("DOMContentLoaded", async () => {
  try {
    // 1. 初始化 LIFF
    await liff.init({ liffId: "2007821360-g5ploEDy" });

    // 2. 取得使用者資訊
    const profile = await liff.getProfile();
    document.getElementById("userId").value = profile.userId;
    document.getElementById("displayName").value = profile.displayName;

    // 3. 綁定送出事件
    document.getElementById("bookingForm").addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        userId: document.getElementById("userId").value,
        displayName: document.getElementById("displayName").value,
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        timeslot: document.getElementById("timeslot").value,
        houseId: document.getElementById("houseId").value,
        houseTitle: document.getElementById("houseTitle").value,
      };

      try {
        const res = await fetch("/api/booking", {
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
        console.error("[book.js] error:", err);
        alert("❌ 發生錯誤，請稍後再試");
      }
    });
  } catch (err) {
    console.error("[book.js] LIFF init error:", err);
    alert("❌ LIFF 初始化失敗");
  }
});
