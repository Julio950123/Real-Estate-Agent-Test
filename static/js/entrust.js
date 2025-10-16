async function postJSON(url = "", data = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json;charset=utf-8" },
    body: JSON.stringify(data),
  });
  const json = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = json.message || "提交失敗，請稍後再試";
    throw new Error(msg);
  }
  return json;
}

function toast(msg, isError = false) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.className = "toast" + (isError ? " error" : "");
  el.style.display = "block";
}

document.getElementById("entrustForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const btn = document.getElementById("submitBtn");
  btn.disabled = true;

  const payload = {
    area: document.getElementById("area").value.trim(),
    community: document.getElementById("community").value.trim(),
    layout: document.getElementById("layout").value.trim(),
    size: document.getElementById("size").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    user_id: document.getElementById("user_id").value.trim(),
  };

  try {
    const result = await postJSON("/submit_entrust", payload);
    // 成功訊息（你要的那段話）
    toast(result.message || "✅ 收到你的資料了！之後會提供初估行情給你～");
    // 若在 LIFF 裡，可自動關閉視窗：
    // if (window.liff && liff.closeWindow) setTimeout(() => liff.closeWindow(), 1200);
  } catch (err) {
    toast(`❌ ${err.message}`, true);
  } finally {
    btn.disabled = false;
  }
});