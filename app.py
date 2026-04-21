"""Web UI and JSON API for Luhn check-digit completion."""

from __future__ import annotations

from flask import Flask, jsonify, render_template, request

from luhn import luhn_check_digit, luhn_complete, luhn_is_valid, luhn_trace
from schemes import (
    SCHEMES,
    expected_body_length,
    matching_schemes,
    scheme_for_id,
    suggested_lengths_for_prefix,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", schemes=SCHEMES)


@app.post("/api/check-digit")
def api_check_digit():
    data = request.get_json(silent=True) or {}
    body = str(data.get("body", ""))
    scheme_id = data.get("scheme")

    digits = "".join(c for c in body if c.isdigit())
    if not digits:
        return jsonify({"error": "Enter at least one digit (check digit omitted)."}), 400

    want_trace = bool(data.get("trace"))

    try:
        check = luhn_check_digit(digits)
        trace_payload = luhn_trace(digits) if want_trace else None
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    full = digits + str(check)
    schemes = matching_schemes(digits)
    scheme_ids = [s.id for s in schemes]
    lengths_hint = suggested_lengths_for_prefix(digits)

    expected = None
    if scheme_id:
        exp = expected_body_length(scheme_id)
        if exp is not None and len(digits) != exp:
            sch = scheme_for_id(scheme_id)
            label = sch.label if sch else scheme_id
            expected = {
                "body_digits": exp,
                "message": f"{label} uses {exp + 1} digits total; you entered {len(digits)} before the check digit.",
            }

    payload = {
        "body": digits,
        "check_digit": check,
        "full_number": full,
        "valid_if_completed": luhn_is_valid(full),
        "matching_scheme_ids": scheme_ids,
        "suggested_total_lengths": list(lengths_hint),
        "length_warning": expected,
    }
    if trace_payload is not None:
        payload["trace"] = trace_payload
    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
