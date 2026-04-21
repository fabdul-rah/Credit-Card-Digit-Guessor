"""CLI: compute the Luhn check digit for digits entered *without* the final check digit."""

from luhn import luhn_check_digit, luhn_complete, luhn_is_valid
from schemes import matching_schemes, suggested_lengths_for_prefix


def main() -> None:
    raw = input("Enter all digits except the final check digit (spaces OK): ").strip()
    digits = "".join(c for c in raw if c.isdigit())
    if not digits:
        print("You need at least one digit.")
        return

    try:
        last = luhn_check_digit(digits)
    except ValueError as e:
        print(e)
        return

    full = luhn_complete(digits)
    schemes = matching_schemes(digits)
    labels = ", ".join(s.label for s in schemes if s.id != "unknown") or schemes[-1].label
    lengths = suggested_lengths_for_prefix(digits)

    print("Digits (check omitted):", digits)
    print("Detected network(s):", labels)
    print("Typical total lengths (digits):", ", ".join(str(n) for n in lengths))
    print("Check digit:", last)
    print("Full number:", full)
    print("Luhn valid:", luhn_is_valid(full))


if __name__ == "__main__":
    main()
