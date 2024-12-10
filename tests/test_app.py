from unittest.mock import patch
import pytest
import asyncio

# Import the test client from conftest
from tests.conftest import client, DatabaseClient_instance, model

# Define Russian test texts
test_texts = [
    ("Отличный продукт", "positive"),
    ("Плохой сервис", "negative"),
    ("Нормально", "neutral")
]


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_predict_form():
    headers = {"Accept": "text/html"}
    for text, expected_sentiment in test_texts:
        # Mock model.predict to return the expected sentiment
        model.predict.return_value = (["test"], (expected_sentiment, 0.9))
        response = client.post("/predict", headers=headers,
                               data={"review_text": text})
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert expected_sentiment in response.text


def test_predict_json():
    headers = {"Accept": "application/json"}
    for text, expected_sentiment in test_texts:
        # Mock model.predict to return the expected sentiment
        model.predict.return_value = (["test"], (expected_sentiment, 0.9))
        response = client.post("/predict", data={"review_text": text})
        assert response.status_code == 200
        assert response.json() == {
            "predictions": {
                "review": text.strip(),
                "sentiment_text": expected_sentiment,
                "sentiment_prob": 0.9,
            }
        }


def test_predict_batch():
    review_texts = [text for text, _ in test_texts]
    expected_predictions = [
        {"review_text": text, "sentiment_text": sentiment, "sentiment_prob": 0.9}
        for text, sentiment in test_texts
    ]
    with patch(
        "api.predict_single_review",
        side_effect=lambda x, y: {
            "review_text": x,
            "sentiment_text": next(sent for text, sent in test_texts if text == x),
            "sentiment_prob": 0.9,
        },
    ):
        response = client.post(
            "/predict-batch", data=review_texts)
        assert response.status_code == 200
        assert response.json() == {"predictions": expected_predictions}
