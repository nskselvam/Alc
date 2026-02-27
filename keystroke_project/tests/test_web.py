import pytest
# make sure the package root (parent of this tests folder) is on sys.path
import os, sys
# two levels up from tests/ is the workspace root containing
# the keystroke_project package directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from keystroke_project.app import app as flask_app


def test_report_endpoint():
    # use the Flask test client to call /report
    client = flask_app.test_client()
    res = client.get("/report")
    assert res.status_code == 200
    data = res.get_json()
    # basic structure checks
    assert "accuracy" in data
    assert "classification_report" in data
    assert isinstance(data["accuracy"], float)
    # accuracy should be between 0 and 1
    assert 0.0 <= data["accuracy"] <= 1.0


def test_predict_endpoint():
    client = flask_app.test_client()
    res = client.get("/predict")
    assert res.status_code == 200
    data = res.get_json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)


def test_homepage_contains_buttons():
    client = flask_app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    body = res.get_data(as_text=True)
    assert "btn-report" in body
    assert "btn-predict" in body
    assert "btn-submit" in body


def test_submit_endpoint():
    client = flask_app.test_client()
    sample_events = [
        {"hold_time": 100, "flight_time": 50, "error": 0},
        {"hold_time": 120, "flight_time": 60, "error": 1},
    ]
    res = client.post("/submit", json={"events": sample_events})
    assert res.status_code == 200
    data = res.get_json()
    assert "prediction" in data
    assert isinstance(data["prediction"], list)


def test_submit_empty():
    client = flask_app.test_client()
    res = client.post("/submit", json={})
    assert res.status_code == 400
    assert res.get_json().get("error")


def test_submit_missing_fields():
    client = flask_app.test_client()
    res = client.post("/submit", json={"events": [{"foo":1}]})
    assert res.status_code == 400
    assert "required" in res.get_json().get("error", "")
