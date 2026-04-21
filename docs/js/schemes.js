/** Issuer hints — mirrors `schemes.py` for static GitHub Pages. */

export const SCHEMES = [
  { id: "visa", label: "Visa", lengths: [13, 16, 19] },
  { id: "mastercard", label: "Mastercard", lengths: [16] },
  { id: "amex", label: "American Express", lengths: [15] },
  { id: "discover", label: "Discover", lengths: [16, 19] },
  { id: "diners", label: "Diners Club", lengths: [14, 16, 19] },
  { id: "jcb", label: "JCB", lengths: [16, 19] },
  { id: "unionpay", label: "UnionPay", lengths: [16, 17, 18, 19] },
  { id: "unknown", label: "Unknown / other", lengths: Array.from({ length: 9 }, (_, i) => i + 12) },
];

function prefixInt(prefix, width) {
  const p = [...prefix].filter((c) => c >= "0" && c <= "9").join("");
  if (p.length < width) return null;
  return parseInt(p.slice(0, width), 10);
}

function inRange(n, lo, hi) {
  return n >= lo && n <= hi;
}

export function matchingSchemes(digitPrefix) {
  const p = [...digitPrefix].filter((c) => c >= "0" && c <= "9").join("");
  if (!p) return [...SCHEMES];

  const hits = [];
  const add = (scheme) => {
    if (!hits.includes(scheme)) hits.push(scheme);
  };

  if (p.startsWith("4")) add(SCHEMES.find((s) => s.id === "visa"));
  if (p.startsWith("34") || p.startsWith("37")) add(SCHEMES.find((s) => s.id === "amex"));
  if (p.startsWith("6011") || p.startsWith("65")) add(SCHEMES.find((s) => s.id === "discover"));
  const n3 = prefixInt(p, 3);
  if (n3 != null && inRange(n3, 644, 649)) add(SCHEMES.find((s) => s.id === "discover"));
  if (p.startsWith("36") || p.startsWith("38")) add(SCHEMES.find((s) => s.id === "diners"));
  const n3d = prefixInt(p, 3);
  if (n3d != null && inRange(n3d, 300, 305)) add(SCHEMES.find((s) => s.id === "diners"));
  const n4 = prefixInt(p, 4);
  if (n4 != null && inRange(n4, 3528, 3589)) add(SCHEMES.find((s) => s.id === "jcb"));
  if (p.startsWith("62")) add(SCHEMES.find((s) => s.id === "unionpay"));
  const n2 = prefixInt(p, 2);
  if (n2 != null && inRange(n2, 51, 55)) add(SCHEMES.find((s) => s.id === "mastercard"));
  if (n4 != null && inRange(n4, 2221, 2720)) add(SCHEMES.find((s) => s.id === "mastercard"));

  if (!hits.length) add(SCHEMES.find((s) => s.id === "unknown"));
  return hits;
}

export function suggestedLengthsForPrefix(digitPrefix) {
  const schemes = matchingSchemes(digitPrefix);
  const lengths = new Set();
  for (const s of schemes) {
    if (s.id === "unknown") continue;
    for (const L of s.lengths) lengths.add(L);
  }
  if (lengths.size) return [...lengths].sort((a, b) => a - b);
  return Array.from({ length: 7 }, (_, i) => i + 13);
}

export function schemeForId(schemeId) {
  return SCHEMES.find((s) => s.id === schemeId) ?? null;
}

export function expectedBodyLength(schemeId) {
  const s = schemeForId(schemeId);
  if (!s || s.id === "unknown") return null;
  if (s.lengths.length !== 1) return null;
  return s.lengths[0] - 1;
}
