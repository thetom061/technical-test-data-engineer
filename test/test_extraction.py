import requests
from src.etl.extract import fetch_all_pages
from unittest.mock import patch

@patch("requests.get")
def test_fetch_all_pages_http_error(mock_get,caplog):
    # Simulate an HTTPError
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")

    with caplog.at_level("ERROR"):  # Ensure ERROR logs are captured
        result = fetch_all_pages("http://fakeurl", page_size=2)

    assert result == []
    assert "HTTP Error occurred:" in caplog.text

@patch("requests.get")
def test_fetch_all_pages_invalid_json(mock_get, caplog):
    # Simulate a response with invalid JSON
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

    with caplog.at_level("ERROR"):  # Ensure ERROR logs are captured
        result = fetch_all_pages("http://fakeurl", page_size=2)

    assert result == []
    assert "Invalid JSON from URL" in caplog.text

@patch("requests.get")
def test_fetch_all_pages_empty(mock_get, caplog):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {
            "items": [],
            "page": 1,
            "size": 2,
            "pages": 1
        }
    ]

    result = fetch_all_pages("http://fakeurl", page_size=2)
    assert result == []
    assert "No items found on page" in caplog.text

@patch("requests.get")
def test_fetch_all_pages_missing_pages(mock_get, caplog):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {
            "items": [{"id": 1}],
            "page": 1,
            "size": 2,
        },
        {
            "items": [{"id": 2}],
            "page": 2,
            "size": 2,
        }
    ]

    result = fetch_all_pages("http://fakeurl", page_size=2)
    assert len(result) == 1
    assert "Number of pages not found for" in caplog.text




@patch("requests.get")
def test_fetch_all_pages_success(mock_get):
    # Simulate first page response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {
            "items": [{"id": 1}, {"id": 2}],
            "page": 1,
            "size": 2,
            "pages": 2
        },
        {
            "items": [{"id": 3}, {"id": 4}],
            "page": 2,
            "size": 2,
            "pages": 2
        }
    ]

    result = fetch_all_pages("http://fakeurl", page_size=2)
    assert len(result) == 4
    assert result[0]["id"] == 1
    assert result[-1]["id"] == 4
