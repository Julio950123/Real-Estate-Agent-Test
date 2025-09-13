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

    // Firestore 抓資料後
    const ref = doc(db, "listings", docId);
    const snap = await getDoc(ref);

    if (!snap.exists()) {
    alert("❌ 找不到物件資料");
    return;
    }
    const data = snap.data();

    const flexMessage = {
    type: "flex",
    altText: `分享物件：${data.title || "好宅"}`,
    contents: {
        type: "bubble",
        size: "mega",
        hero: {
        type: "image",
        url: data.image_url || "https://picsum.photos/800/520",
        size: "full",
        aspectRatio: "20:13",
        aspectMode: "cover"
        },
        body: {
        type: "box",
        layout: "vertical",
        contents: [
            { type: "text", text: data.title || "未命名物件", weight: "bold", size: "lg" },
            { type: "text", text: data.address || "-", size: "sm", color: "#7B7B7B" },
            { type: "text", text: `${data.square_meters || "?"}坪｜${data.genre || "-"}`, size: "sm", color: "#555555" },
            { type: "text", text: `${data.price || "?"} 萬 (含車位)`, size: "md", weight: "bold", color: "#FF5809" }
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