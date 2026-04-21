/** Luhn (mod 10) — mirrors `luhn.py` for static GitHub Pages builds. */

export function digitsOnly(s) {
  return [...s].filter((c) => c >= "0" && c <= "9").join("");
}

export function luhnCheckDigit(body) {
  const d = digitsOnly(body);
  if (!d.length) {
    throw new Error("Need at least one digit before the check digit.");
  }
  const digits = [...d].map((c) => parseInt(c, 10));
  const lengthWithCheck = digits.length + 1;
  let total = 0;
  for (let i = digits.length - 1; i >= 0; i--) {
    let v = digits[i];
    const posFromRight = lengthWithCheck - i;
    if (posFromRight % 2 === 0) {
      v *= 2;
      if (v > 9) v -= 9;
    }
    total += v;
  }
  return (10 - (total % 10)) % 10;
}

export function luhnComplete(body) {
  const d = digitsOnly(body);
  return d + String(luhnCheckDigit(d));
}

export function luhnIsValid(pan) {
  const d = digitsOnly(pan);
  if (d.length < 2) return false;
  const body = d.slice(0, -1);
  const check = parseInt(d.slice(-1), 10);
  return luhnCheckDigit(body) === check;
}

export function luhnTrace(body) {
  const d = digitsOnly(body);
  if (!d.length) {
    throw new Error("Need at least one digit before the check digit.");
  }
  const digits = [...d].map((c) => parseInt(c, 10));
  const n = digits.length;
  const lengthWithCheck = n + 1;
  const steps = [];
  let total = 0;
  for (let i = 0; i < n; i++) {
    const v = digits[i];
    const posFromRight = lengthWithCheck - i;
    const doubled = posFromRight % 2 === 0;
    let contribution;
    if (doubled) {
      const raw = v * 2;
      contribution = raw > 9 ? raw - 9 : raw;
    } else {
      contribution = v;
    }
    total += contribution;
    steps.push({
      index_from_left: i,
      position_from_right: posFromRight,
      digit: v,
      doubled,
      contribution,
    });
  }
  const checkDigit = (10 - (total % 10)) % 10;
  return {
    body: d,
    steps,
    sum_transformed_body: total,
    check_digit: checkDigit,
  };
}
