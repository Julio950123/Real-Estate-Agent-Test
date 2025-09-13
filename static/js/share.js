// 初始化 Firebase
const app = firebase.initializeApp(firebaseConfig);
const db = firebase.firestore(app);

async function main() {
  await liff.init({ liffId: "2007821360-5zM287yq" });
  console.log("要分享的物件ID:", listingId);

  // 從 Firestore 讀取物件
  const doc = await db.collection("listings").doc(listingId).get();
  const data = doc.data();

  const bubble = {
    type: "bubble",
    hero: {
      type: "image",
      url: data.image_url || "https://via.placeholder.com/300x200",
      size: "full",
      aspectRatio: "20:13",
      aspectMode: "cover"
    },
    body: {
      type: "box",
      layout: "vertical",
      contents: [
        { type: "text", text: data.title || "未命名物件", weight: "bold", size: "lg" },
        { type: "text", text: `${data.square_meters || '-'}坪｜${data.genre || '-'}`, size: "sm", color: "#888888" },
        { type: "text", text: `${data.price || '-'}萬`, weight: "bold", size: "lg", color: "#FF5809" }
      ]
    }
  };

  await liff.shareTargetPicker([
    { type: "flex", altText: "快來看這個物件！", contents: bubble }
  ]);

  liff.closeWindow();
}

main();
