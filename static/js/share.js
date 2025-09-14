// 🔹 LIFF ID
const LIFF_ID = "2007821360-5zM287yq"; // ⚠️ 換成你的 LIFF ID

// 🔹 Firebase Config
const firebaseConfig = {
  apiKey: "你的-APIKEY",
  authDomain: "real-estate-agent-test-d1300.firebaseapp.com",
  projectId: "real-estate-agent-test-d1300"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// 取得網址參數
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

async function main() {
  try {
    await liff.init({ liffId: LIFF_ID });

    if (!liff.isLoggedIn()) {
      liff.login();
      return;
    }

    const docId = getQueryParam("doc_id");
    if (!docId) {
      document.getElementById("status").innerText = "❌ 缺少 doc_id 參數";
      return;
    }

    const snap = await db.collection("listings").doc(docId).get();
    if (!snap.exists) {
      document.getElementById("status").innerText = "❌ 找不到物件資料";
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
    },
    footer: {
      type: "box",
      layout: "vertical",
      spacing: "md",
      contents: [
        {
          type: "button",
          style: "primary",
          color: "#06C755", // LINE 綠色
          action: {
            type: "uri",
            label: "加入這個LINE@好友",
            uri: "https://line.me/R/ti/p/@123abcd" // ⚠️ 改成你的 LINE 官方帳號 ID
          }
        }
      ]
    }
  }
};
    document.getElementById("status").innerText = "載入完成，正在開啟分享...";

    await liff.shareTargetPicker([flexMessage]);
    setTimeout(() => liff.closeWindow(), 1200);

  } catch (err) {
    console.error("❌ LIFF 初始化失敗:", err);
    document.getElementById("status").innerText = "⚠️ LIFF 初始化失敗，請重新開啟連結";
  }
}

main();
