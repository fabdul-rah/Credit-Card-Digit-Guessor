import pytest

from luhn import luhn_check_digit, luhn_complete, luhn_is_valid, luhn_trace


def test_wikipedia_example():
    assert luhn_check_digit("7992739871") == 3
    assert luhn_complete("7992739871") == "79927398713"
    assert luhn_is_valid("79927398713")


def test_visa_like_16():
    body = "453201511283036"
    assert luhn_check_digit(body) == 6
    assert luhn_is_valid(luhn_complete(body))


def test_amex_15_digit_pan():
    body = "37828224631000"
    assert luhn_check_digit(body) == 5
    assert luhn_is_valid("378282246310005")


def test_rejects_old_wrong_parity_for_amex():
    """Old script doubled even indices from the left — wrong for 14-digit body."""
    body = "37828224631000"
    wrong_even_index_rule = _legacy_wrong_check(body)
    assert wrong_even_index_rule != luhn_check_digit(body)


def _legacy_wrong_check(card_input: str) -> int:
    odd_doubled = []
    even_nums = []
    for i, char in enumerate(card_input):
        if i % 2 == 0:
            v = int(char) * 2
            odd_doubled.append(v // 10 + v % 10 if v > 9 else v)
        else:
            even_nums.append(int(char))
    total = sum(odd_doubled) + sum(even_nums)
    return (10 - (total % 10)) % 10


def test_full_valid_pan():
    assert luhn_is_valid("5555555555554444")


def test_invalid_pan():
    assert not luhn_is_valid("5555555555554445")


def test_raises_on_empty_body():
    with pytest.raises(ValueError):
        luhn_check_digit("")


def test_trace_matches_check_digit():
    body = "7992739871"
    t = luhn_trace(body)
    assert t["check_digit"] == luhn_check_digit(body)
    assert t["sum_transformed_body"] == sum(s["contribution"] for s in t["steps"])
    assert len(t["steps"]) == len(body)


def test_trace_amex_body():
    body = "37828224631000"
    t = luhn_trace(body)
    assert t["check_digit"] == 5
    assert t["steps"][0]["position_from_right"] == 15
