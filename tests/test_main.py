import pytest
from fastapi.testclient import TestClient

from app import app, days_without_issues_counter, days_without_drama_counter

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Days without issues" in response.text
    assert "Days without drama" in response.text


def test_push_drama():
    payload = {"days": 7}
    response = client.post("/push_drama", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Days without drama has been pushed by 7 days"}
    assert days_without_drama_counter._value.get() == 7


def test_push_issues():
    payload = {"days": 3}
    response = client.post("/push_issues", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Days without issues has been pushed by 3 days"}
    assert days_without_issues_counter._value.get() == 3


def test_push_drama_negative_days():
    payload = {"days": -1}
    response = client.post("/push_drama", json=payload)
    assert response.status_code == 400
    assert "Invalid number of days" in response.text
    assert days_without_drama_counter._value.get() == 7


def test_push_issues_negative_days():
    payload = {"days": -1}
    response = client.post("/push_issues", json=payload)
    assert response.status_code == 400
    assert "Invalid number of days" in response.text
    assert days_without_issues_counter._value.get() == 3
