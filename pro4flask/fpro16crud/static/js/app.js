console.log("app.js loaded");
console.log("API_LIST =", window.API_LIST);

const $ = (sel) => document.querySelector(sel);

const els = {
  code: $("#code"),
  sang: $("#sang"),
  su: $("#su"),
  dan: $("#dan"),
  msg: $("#msg"),
  tbody: $("#tbody"),
  btnAdd: $("#btnAdd"),
  btnUpdate: $("#btnUpdate"),
  btnDelete: $("#btnDelete"),
  btnClear: $("#btnClear"),
  btnReload: $("#btnReload"),
};

function setMsg(text, isError = false) {
  els.msg.textContent = text;
  els.msg.classList.toggle("error", isError);
}

function getForm() {
  return {
    code: els.code.value.trim(),
    sang: els.sang.value.trim(),
    su: els.su.value.trim(),
    dan: els.dan.value.trim(),
  };
}

function clearForm() {
  els.code.value = "";
  els.sang.value = "";
  els.su.value = "";
  els.dan.value = "";
  setMsg("초기화 완료");
}

function renderRows(rows) {
  els.tbody.innerHTML = rows.map(r => `
    <tr data-code="${r.code}">
      <td>${r.code}</td>
      <td>${r.sang ?? ""}</td>
      <td>${r.su ?? ""}</td>
      <td>${r.dan ?? ""}</td>
    </tr>
  `).join("");
}

async function loadAll() {
  setMsg("조회 중...");

  try {
    const url = "/api/sangdata?_=" + Date.now();
    console.log("fetch url =", url);

    const res = await fetch(url, {
      method: "GET",
      headers: { "Accept": "application/json" },
      cache: "no-store"
    });

    console.log("res.url =", res.url);
    console.log("status =", res.status);
    console.log("content-type =", res.headers.get("content-type"));

    const text = await res.text();
    console.log("body =", text);

    const data = JSON.parse(text);

    if (!res.ok || data.ok === false) {
      throw new Error(data.error || "조회 실패");
    }

    renderRows(data.data);
    setMsg(`조회 완료: ${data.data.length}건`);
  } catch (e) {
    setMsg(`조회 오류: ${e.message}`, true);
  }
}

async function addOne() {
  const f = getForm();
  if (!f.code || !f.sang) return setMsg("code, sang는 필수!", true);

  try {
    const res = await fetch("/api/sangdata", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        code: Number(f.code),
        sang: f.sang,
        su: Number(f.su || 0),
        dan: Number(f.dan || 0),
      })
    });

    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "추가 실패");

    setMsg(`추가 완료: code=${data.code}`);
    await loadAll();
  } catch (e) {
    setMsg(`추가 오류: ${e.message}`, true);
  }
}

async function updateOne() {
  const f = getForm();
  if (!f.code) return setMsg("수정하려면 code가 필요!", true);

  try {
    const res = await fetch(`/api/sangdata/${Number(f.code)}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({
        sang: f.sang,
        su: Number(f.su || 0),
        dan: Number(f.dan || 0),
      })
    });

    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "수정 실패");

    setMsg(`수정 완료: code=${data.code}`);
    await loadAll();
  } catch (e) {
    setMsg(`수정 오류: ${e.message}`, true);
  }
}

async function deleteOne() {
  const f = getForm();
  if (!f.code) return setMsg("삭제하려면 code가 필요!", true);
  if (!confirm(`code=${f.code}를 삭제할까요?`)) return;

  try {
    const res = await fetch(`/api/sangdata/${Number(f.code)}`, {
      method: "DELETE",
      headers: { "Accept": "application/json" }
    });

    const data = await res.json();
    if (!res.ok || data.ok === false) throw new Error(data.error || "삭제 실패");

    setMsg(`삭제 완료: code=${data.code}`);
    clearForm();
    await loadAll();
  } catch (e) {
    setMsg(`삭제 오류: ${e.message}`, true);
  }
}

els.tbody.addEventListener("click", (e) => {
  const tr = e.target.closest("tr");
  if (!tr) return;

  const tds = tr.querySelectorAll("td");
  els.code.value = tds[0].textContent;
  els.sang.value = tds[1].textContent;
  els.su.value = tds[2].textContent;
  els.dan.value = tds[3].textContent;
  setMsg(`선택됨: code=${els.code.value}`);
});

els.btnReload.addEventListener("click", loadAll);
els.btnClear.addEventListener("click", clearForm);
els.btnAdd.addEventListener("click", addOne);
els.btnUpdate.addEventListener("click", updateOne);
els.btnDelete.addEventListener("click", deleteOne);

window.addEventListener("DOMContentLoaded", loadAll);