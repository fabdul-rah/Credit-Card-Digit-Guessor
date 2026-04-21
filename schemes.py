"""Major card brands — expected lengths and prefix rules (simplified BIN/IIN)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class CardScheme:
    id: str
    label: str
    lengths: tuple[int, ...]
    primary_color: str
    accent_color: str

    def accepts_length(self, n: int) -> bool:
        return n in self.lengths


SCHEMES: tuple[CardScheme, ...] = (
    CardScheme(
        "visa",
        "Visa",
        (13, 16, 19),
        "#1a1f71",
        "#ffffff",
    ),
    CardScheme(
        "mastercard",
        "Mastercard",
        (16,),
        "#eb001b",
        "#f79e1b",
    ),
    CardScheme(
        "amex",
        "American Express",
        (15,),
        "#006fcf",
        "#ffffff",
    ),
    CardScheme(
        "discover",
        "Discover",
        (16, 19),
        "#ff6000",
        "#ffffff",
    ),
    CardScheme(
        "diners",
        "Diners Club",
        (14, 16, 19),
        "#0079be",
        "#ffffff",
    ),
    CardScheme(
        "jcb",
        "JCB",
        (16, 19),
        "#0c4b8e",
        "#ffffff",
    ),
    CardScheme(
        "unionpay",
        "UnionPay",
        (16, 17, 18, 19),
        "#e21836",
        "#ffffff",
    ),
    CardScheme(
        "unknown",
        "Unknown / other",
        tuple(range(12, 21)),
        "#2d3142",
        "#bfc0c0",
    ),
)


def _prefix_int(prefix: str, width: int) -> int | None:
    p = "".join(c for c in prefix if c.isdigit())
    if len(p) < width:
        return None
    return int(p[:width])


def _in_range(n: int, lo: int, hi: int) -> bool:
    return lo <= n <= hi


def matching_schemes(digit_prefix: str) -> list[CardScheme]:
    """
    Return schemes consistent with the typed digit prefix (most specific first).
    Always ends with `unknown` if nothing else matched.
    """
    p = "".join(c for c in digit_prefix if c.isdigit())
    if not p:
        return list(SCHEMES)

    hits: list[CardScheme] = []

    def add(scheme: CardScheme) -> None:
        if scheme not in hits:
            hits.append(scheme)

    # Visa — 4
    if p.startswith("4"):
        add(next(s for s in SCHEMES if s.id == "visa"))

    # AmEx — 34, 37
    if p.startswith("34") or p.startswith("37"):
        add(next(s for s in SCHEMES if s.id == "amex"))

    # Discover — 6011, 65, 644–649
    if p.startswith("6011") or p.startswith("65"):
        add(next(s for s in SCHEMES if s.id == "discover"))
    n3 = _prefix_int(p, 3)
    if n3 is not None and _in_range(n3, 644, 649):
        add(next(s for s in SCHEMES if s.id == "discover"))

    # Diners — 36, 38, 300–305
    if p.startswith("36") or p.startswith("38"):
        add(next(s for s in SCHEMES if s.id == "diners"))
    n3d = _prefix_int(p, 3)
    if n3d is not None and _in_range(n3d, 300, 305):
        add(next(s for s in SCHEMES if s.id == "diners"))

    # JCB — 3528–3589
    n4 = _prefix_int(p, 4)
    if n4 is not None and _in_range(n4, 3528, 3589):
        add(next(s for s in SCHEMES if s.id == "jcb"))

    # UnionPay — 62
    if p.startswith("62"):
        add(next(s for s in SCHEMES if s.id == "unionpay"))

    # Mastercard — 51–55, 2221–2720
    n2 = _prefix_int(p, 2)
    if n2 is not None and _in_range(n2, 51, 55):
        add(next(s for s in SCHEMES if s.id == "mastercard"))
    if n4 is not None and _in_range(n4, 2221, 2720):
        add(next(s for s in SCHEMES if s.id == "mastercard"))

    if not hits:
        add(next(s for s in SCHEMES if s.id == "unknown"))
    return hits


def suggested_lengths_for_prefix(digit_prefix: str) -> tuple[int, ...]:
    schemes = matching_schemes(digit_prefix)
    lengths: set[int] = set()
    for s in schemes:
        if s.id == "unknown":
            continue
        lengths.update(s.lengths)
    if lengths:
        return tuple(sorted(lengths))
    return tuple(range(13, 20))


def scheme_for_id(scheme_id: str) -> CardScheme | None:
    for s in SCHEMES:
        if s.id == scheme_id:
            return s
    return None


def expected_body_length(scheme_id: str) -> int | None:
    """Digits *before* check digit for a fixed-length brand, if unambiguous."""
    s = scheme_for_id(scheme_id)
    if not s or s.id == "unknown":
        return None
    if len(s.lengths) != 1:
        return None
    return s.lengths[0] - 1
