// 測試用最小版 share.js

// 🔹 你的 LIFF ID
const LIFF_ID = "2007821360-5zM287yq";  // ⚠️ 換成你的 LIFF ID

// 取得網址參數
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

async function main() {
  try {
    // 初始化 LIFF
    await liff.init({ liffId: LIFF_ID });

    if (!liff.isLoggedIn()) {
      liff.login();
      return;
    }

    // 讀取 doc_id
    const docId = getQueryParam("doc_id") || "❌ 沒有 doc_id";
    console.log("📌 測試 doc_id =", docId);
    alert("測試 doc_id = " + docId);

    // 建立測試用 Flex Message
    const flexMessage = {
      type: "flex",
      altText: "測試分享",
      contents: {
        type: "bubble",
        body: {
          type: "box",
          layout: "vertical",
          contents: [
            { type: "text", text: "✅ 測試成功！", weight: "bold", size: "lg", color: "#06C755" },
            { type: "text", text: "doc_id=" + docId, size: "sm", color: "#555555" }
          ]
        }
      }
    };

    // 嘗試分享
    await liff.shareTargetPicker([flexMessage])
      .then(() => {
        console.log("✅ 已分享");
        liff.closeWindow();
      })
      .catch(err => {
        console.error("❌ 分享失敗:", err);
        alert("分享失敗: " + err);
      });

  } catch (error) {
    console.error("❌ LIFF 初始化失敗:", error);
    alert("LIFF 初始化失敗: " + error);
  }
}

main();
