"""Luhn (mod 10) check digit — correct for any partial length before the check digit."""


def _digits_only(s: str) -> str:
    return "".join(c for c in s if c.isdigit())


def luhn_check_digit(body: str) -> int:
    """
    Return the check digit (0–9) for a PAN *without* its final check digit.

    Doubling starts at the digit immediately left of the check digit (the
    rightmost digit of the full number is never doubled).
    """
    digits = [int(c) for c in _digits_only(body)]
    if not digits:
        raise ValueError("Need at least one digit before the check digit.")

    total = 0
    length_with_check = len(digits) + 1
    for i in range(len(digits) - 1, -1, -1):
        v = digits[i]
        pos_from_right = length_with_check - i
        if pos_from_right % 2 == 0:
            v *= 2
            if v > 9:
                v -= 9
        total += v
    return (10 - (total % 10)) % 10


def luhn_complete(body: str) -> str:
    """Append the correct check digit to the body (digits only)."""
    d = _digits_only(body)
    return d + str(luhn_check_digit(d))


def luhn_is_valid(pan: str) -> bool:
    """True if the full PAN satisfies the Luhn checksum."""
    d = _digits_only(pan)
    if len(d) < 2:
        return False
    body, check = d[:-1], int(d[-1])
    return luhn_check_digit(body) == check


def luhn_trace(body: str) -> dict:
    """
    Per-digit breakdown for teaching: contribution of each body digit toward
    the check digit, using the same rules as ``luhn_check_digit``.
    """
    d = _digits_only(body)
    digits = [int(c) for c in d]
    if not digits:
        raise ValueError("Need at least one digit before the check digit.")

    n = len(digits)
    length_with_check = n + 1
    steps: list[dict] = []
    total = 0
    for i in range(n):
        v = digits[i]
        pos_from_right = length_with_check - i
        doubled = pos_from_right % 2 == 0
        if doubled:
            raw = v * 2
            contribution = raw - 9 if raw > 9 else raw
        else:
            contribution = v
        total += contribution
        steps.append(
            {
                "index_from_left": i,
                "position_from_right": pos_from_right,
                "digit": v,
                "doubled": doubled,
                "contribution": contribution,
            }
        )
    check = (10 - (total % 10)) % 10
    return {
        "body": d,
        "steps": steps,
        "sum_transformed_body": total,
        "check_digit": check,
    }
