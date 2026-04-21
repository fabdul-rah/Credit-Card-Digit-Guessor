const bodyEl = document.getElementById("body");
const schemeEl = document.getElementById("scheme");
const resultsEl = document.getElementById("results");
const checkEl = document.getElementById("check");
const fullEl = document.getElementById("full");
const chipScheme = document.getElementById("chip-scheme");
const chipLength = document.getElementById("chip-length");
const banner = document.getElementById("banner");
const copyBtn = document.getElementById("copy");
const liveResults = document.getElementById("live-results");
const traceTable = document.getElementById("trace-table");
const traceBody = document.getElementById("trace-body");
const traceSum = document.getElementById("trace-sum");
const traceCheck = document.getElementById("trace-check");

const schemeLabels = {
  visa: "Visa",
  mastercard: "Mastercard",
  amex: "American Express",
  discover: "Discover",
  diners: "Diners Club",
  jcb: "JCB",
  unionpay: "UnionPay",
  unknown: "Unknown / other",
};

function showBanner(message) {
  banner.textContent = message;
  banner.hidden = false;
}

function hideBanner() {
  banner.hidden = true;
  banner.textContent = "";
}

function renderTrace(trace) {
  if (!trace || !trace.steps || !trace.steps.length) {
    traceTable.hidden = true;
    traceBody.innerHTML = "";
    return;
  }
  traceBody.innerHTML = "";
  trace.steps.forEach((row, idx) => {
    const tr = document.createElement("tr");
    if (row.doubled) {
      tr.classList.add("trace-row-doubled");
    }
    tr.innerHTML = `
      <td>${idx + 1}</td>
      <td>${row.position_from_right}</td>
      <td>${row.digit}</td>
      <td>${row.doubled ? "Yes" : "No"}</td>
      <td>${row.contribution}</td>
    `;
    traceBody.appendChild(tr);
  });
  traceSum.textContent = String(trace.sum_transformed_body);
  traceCheck.textContent = String(trace.check_digit);
  traceTable.hidden = false;
}

async function refresh() {
  const body = bodyEl.value;
  const scheme = schemeEl.value;

  if (!body.replace(/\D/g, "")) {
    resultsEl.hidden = true;
    hideBanner();
    liveResults.textContent = "";
    traceTable.hidden = true;
    traceBody.innerHTML = "";
    return;
  }

  try {
    const res = await fetch("/api/check-digit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ body, scheme: scheme || null, trace: true }),
    });
    const data = await res.json();
    if (!res.ok) {
      showBanner(data.error || "Something went wrong.");
      resultsEl.hidden = true;
      liveResults.textContent = "";
      traceTable.hidden = true;
      traceBody.innerHTML = "";
      return;
    }
    hideBanner();
    if (data.length_warning) {
      showBanner(data.length_warning.message);
    }
    checkEl.textContent = String(data.check_digit);
    fullEl.textContent = data.full_number;

    const primary = data.matching_scheme_ids[0] || "unknown";
    chipScheme.textContent = schemeLabels[primary] || primary;
    const totals = data.suggested_total_lengths || [];
    chipLength.textContent = totals.length ? `Common lengths: ${totals.join(", ")} digits` : "";

    liveResults.textContent = `Check digit ${data.check_digit}. Full number updated.`;

    renderTrace(data.trace);

    resultsEl.hidden = false;
  } catch {
    showBanner("Network error — is the server running?");
    resultsEl.hidden = true;
    liveResults.textContent = "";
    traceTable.hidden = true;
    traceBody.innerHTML = "";
  }
}

let t = null;
function debounceRefresh() {
  clearTimeout(t);
  t = setTimeout(refresh, 160);
}

bodyEl.addEventListener("input", debounceRefresh);
schemeEl.addEventListener("change", refresh);

copyBtn.addEventListener("click", async () => {
  const text = fullEl.textContent;
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    copyBtn.textContent = "Copied";
    setTimeout(() => {
      copyBtn.textContent = "Copy";
    }, 1500);
  } catch {
    copyBtn.textContent = "Copy failed";
    setTimeout(() => {
      copyBtn.textContent = "Copy";
    }, 1500);
  }
});
