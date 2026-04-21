def test_api_includes_trace_when_requested():
    from app import app

    client = app.test_client()
    res = client.post("/api/check-digit", json={"body": "7992739871", "trace": True})
    assert res.status_code == 200
    data = res.get_json()
    assert data["check_digit"] == 3
    assert "trace" in data
    assert data["trace"]["sum_transformed_body"] == sum(s["contribution"] for s in data["trace"]["steps"])


def test_api_omits_trace_by_default():
    from app import app

    client = app.test_client()
    res = client.post("/api/check-digit", json={"body": "7992739871"})
    assert res.status_code == 200
    assert "trace" not in res.get_json()
