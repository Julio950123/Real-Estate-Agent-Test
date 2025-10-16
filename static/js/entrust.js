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
    layout: document.getElementById("layout").value.trim(),
    size: document.getElementById("size").value.trim(),
    phone: document.getElementById("phone").value.trim(),
    user_id: document.getElementById("user_id").value.trim(),
  };

  try {
    const result = await postJSON("/submit_entrust", payload);
    toast(result.message || "✅ 已收到你的資料囉！我們會盡快提供初估行情 💬");
    setTimeout(() => {
      if (window.liff && liff.closeWindow) liff.closeWindow();
    }, 1600);
  } catch (err) {
    toast(`❌ ${err.message}`, true);
  } finally {
    btn.disabled = false;
  }
});
