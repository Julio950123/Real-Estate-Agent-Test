// share.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-app.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/9.22.2/firebase-firestore.js";

// 🔹 你的 Firebase 設定
const firebaseConfig = {
  apiKey: "xxxx",
  authDomain: "xxxx",
  projectId: "xxxx",
  storageBucket: "xxxx",
  messagingSenderId: "xxxx",
  appId: "xxxx"
};

// 初始化 Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// 抓網址參數
function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

// 生成 Flex Message
function buildFlex(data) {
  return {
    type: "flex",
    altText: `分享物件：${data.title}`,
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
          { type: "text", text: data.title, weight: "bold", size: "lg" },
          { type: "text", text: data.address, size: "sm", color: "#7B7B7B" },
          { type: "text", text: `${data.square_meters}坪｜${data.genre}`, size: "sm", color: "#555555" },
          { type: "text", text: `${data.price} 萬 (含車位)`, size: "md", weight: "bold", color: "#FF5809" }
        ]
      }
    }
  };
}

async function main() {
  const LIFF_ID = "YOUR_LIFF_ID";
  await liff.init({ liffId: LIFF_ID });

  const docId = getQueryParam("doc_id");
  if (!docId) {
    alert("❌ 缺少物件 ID");
    return;
  }

  // 抓 Firestore 資料
  const ref = doc(db, "houses", docId);
  const snap = await getDoc(ref);
  if (!snap.exists()) {
    alert("❌ 找不到物件資料");
    return;
  }

  const data = snap.data();
  const flexMessage = buildFlex(data);

  // 分享
  await liff.shareTargetPicker([flexMessage])
    .then(() => liff.closeWindow())
    .catch(err => console.error("分享失敗:", err));
}

main();