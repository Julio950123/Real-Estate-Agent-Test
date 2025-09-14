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

    // ✅ 把 doc_id 一起塞進 data，避免 undefined
    const data = { ...snap.data(), doc_id: docId };

    // 🔹 Flex Message
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
            {
              type: "box",
              layout: "horizontal",
              contents: [
                {
                  type: "image",
                  url: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
                  size: "sm", // ✅ 改成 sm
                  flex: 8
                },
                {
                  type: "text",
                  text: data.address || "-",
                  flex: 90,
                  color: "#7B7B7B"
                }
              ]
            },
            {
              type: "text",
              text: data.title || "未命名物件",
              weight: "bold",
              size: "lg"
            },
            {
              type: "text",
              text: `${data.square_meters || "?"}坪｜${data.genre || "-"}`,
              size: "sm",
              color: "#555555",
              margin: "sm"
            },
            {
              type: "box",
              layout: "horizontal",
              contents: [
                {
                  type: "box",
                  layout: "horizontal",
                  contents: [
                    {
                      type: "text",
                      text: data.detail1 || "-",
                      align: "center",
                      color: "#7B7B7B"
                    }
                  ],
                  backgroundColor: "#e7e8e7",
                  cornerRadius: "5px",
                  paddingAll: "4px"
                },
                {
                  type: "box",
                  layout: "horizontal",
                  contents: [
                    {
                      type: "text",
                      text: data.detail2 || "-",
                      align: "center",
                      color: "#7B7B7B"
                    }
                  ],
                  backgroundColor: "#e7e8e7",
                  cornerRadius: "5px",
                  paddingAll: "4px"
                }
              ],
              spacing: "md",
              margin: "sm"
            },
            {
              type: "box",
              layout: "horizontal",
              contents: [
                {
                  type: "text",
                  text: "（含車位價格）",
                  size: "sm",
                  weight: "bold",
                  color: "#7B7B7B",
                  align: "end",
                  gravity: "center"
                },
                {
                  type: "text",
                  text: `${data.price || "?"}萬`,
                  size: "xl",
                  weight: "bold",
                  color: "#FF5809",
                  margin: "sm",
                  align: "end"
                }
              ]
            },
            { type: "separator", margin: "sm" }
          ]
        },
        footer: {
          type: "box",
          layout: "vertical",
          spacing: "md",
          contents: [
            {
              type: "box",
              layout: "horizontal",
              spacing: "md",
              contents: [
                {
                  type: "button",
                  height: "sm",
                  flex: 50,
                  color: "#EE9226",
                  style: "primary",
                  action: {
                    type: "message",
                    label: "物件詳情",
                    text: `物件詳情 ${data.title || "未命名物件"}`
                  }
                },
                {
                  type: "button",
                  height: "sm",
                  flex: 25,
                  color: "#9D9D9D",
                  style: "primary",
                  action: {
                    type: "uri",
                    label: "分享",
                    uri: `https://liff.line.me/${LIFF_ID}?doc_id=${encodeURIComponent(data.doc_id)}`
                  }
                }
              ]
            },
            {
              type: "text",
              text: "物件以現場與權狀為主",
              align: "center",
              size: "xs",
              weight: "regular"
            }
          ]
        }
      }
    };

    // 🔹 分享
    document.getElementById("status").innerText = "載入完成，正在開啟分享...";
    await liff.shareTargetPicker([flexMessage]);

    // 關閉視窗
    setTimeout(() => liff.closeWindow(), 1200);

  } catch (err) {
    console.error("❌ LIFF 初始化失敗:", err);
    document.getElementById("status").innerText = "⚠️ LIFF 初始化失敗，請重新開啟連結";
  }
}

main();
