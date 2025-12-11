const form = document.getElementById("prompt-form");
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const sampleButton = document.getElementById("sample-button");
const submitButton = form.querySelector("button[type='submit']");

const API_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://localhost:8000/api/generate"
    : "/api/generate";

const SAMPLE = {
  caution: "크레인 회전 반경 내 출입 금지, 신호수 지시에 따라 이동",
  location: "3동 옥상 방수 보강 구간",
  checks: "공구 정리, 난간 고정 상태 확인, 폐기물 분리배출, 안전대 훅 분리 후 회수",
};

function setStatus(message) {
  statusEl.textContent = message || "";
}

function setLoading(isLoading) {
  submitButton.disabled = isLoading;
  submitButton.textContent = isLoading ? "이미지 생성 중..." : "5개 언어로 이미지 만들기";
}

function renderEmpty() {
  resultsEl.innerHTML = `<div class="empty">출력된 이미지가 없습니다. 내용을 입력하고 생성해보세요.</div>`;
}

function renderCards(images) {
  if (!images || images.length === 0) {
    renderEmpty();
    return;
  }

  resultsEl.innerHTML = images
    .map(
      (img) => `
      <article class="card">
        <div class="chip">${img.label}</div>
        <img src="${img.image}" alt="${img.label} safety poster" loading="lazy" />
        <div class="translation">
          <dl>
            <dt>오늘의 주의사항</dt>
            <dd>${img.translation.caution}</dd>
            <dt>위치</dt>
            <dd>${img.translation.location}</dd>
            <dt>마무리 작업 시 필수 확인사항</dt>
            <dd>${img.translation.checks}</dd>
          </dl>
        </div>
      </article>
    `
    )
    .join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  setLoading(true);
  setStatus("OpenAI 이미지 생성 중입니다. 언어별 번역 후 이미지를 만듭니다...");
  resultsEl.innerHTML = "";

  const payload = {
    caution: form.caution.value.trim(),
    location: form.location.value.trim(),
    checks: form.checks.value.trim(),
    size: form.size.value,
  };

  if (!payload.caution || !payload.location || !payload.checks) {
    setStatus("모든 필드를 입력해주세요.");
    setLoading(false);
    return;
  }

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(errorText || "이미지를 가져오지 못했습니다.");
    }

    const data = await response.json();
    renderCards(data.images);
    setStatus("완료! 언어별 번역과 이미지 생성이 끝났습니다.");
  } catch (error) {
    console.error(error);
    setStatus(`오류가 발생했습니다: ${error.message}`);
    renderEmpty();
  } finally {
    setLoading(false);
  }
});

sampleButton.addEventListener("click", () => {
  form.caution.value = SAMPLE.caution;
  form.location.value = SAMPLE.location;
  form.checks.value = SAMPLE.checks;
  setStatus("샘플 값이 입력되었습니다. 바로 생성해 보세요.");
});

renderEmpty();
