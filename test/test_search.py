from unittest.mock import patch, MagicMock
import pytest
from riplex.services.search import search_web
from riplex.schemas.research import Source


def test_search_web_success():
    mock_response = {
        "results": [
            {
                "title": "Python 3.14 Features",
                "url": "https://docs.python.org/3.14/",
                "content": "Python 3.14 is the latest version with new features.",
                "publication_date": "2026-10-15",
            },
            {
                "title": "AI Trends 2026",
                "url": "https://example.com/ai-trends",
                "content": "Key trends in AI for 2026.",
                "publication_date": None,
            },
        ]
    }

    with patch("riplex.services.search.client.search", return_value=mock_response) as mock_search:
        sources = search_web("Python 3.14", num_results=2)

        mock_search.assert_called_once_with("Python 3.14", search_depth="basic", max_results=2)
        assert len(sources) == 2
        assert isinstance(sources[0], Source)
        assert sources[0].title == "Python 3.14 Features"
        assert str(sources[0].url) == "https://docs.python.org/3.14/"
        assert sources[0].snippet == "Python 3.14 is the latest version with new features."
        assert sources[0].publication_date == "2026-10-15"

        assert sources[1].title == "AI Trends 2026"
        assert str(sources[1].url) == "https://example.com/ai-trends"
        assert sources[1].snippet == "Key trends in AI for 2026."
        assert sources[1].publication_date is None


def test_search_web_default_num_results():
    with patch("riplex.services.search.client.search", return_value={"results": []}) as mock_search:
        sources = search_web("Default search")

        mock_search.assert_called_once_with("Default search", search_depth="basic", max_results=5)
        assert sources == []


def test_search_web_empty_results():
    with patch("riplex.services.search.client.search", return_value={}):
        sources = search_web("No results query")
        assert sources == []


def test_search_web_snippet_truncation():
    long_content = "x" * 5000
    mock_response = {
        "results": [
            {
                "title": "Long Page",
                "url": "https://example.com/long",
                "content": long_content,
            }
        ]
    }

    with patch("riplex.services.search.client.search", return_value=mock_response):
        sources = search_web("Long content test")
        assert len(sources) == 1
        assert len(sources[0].snippet) == 2000
        assert sources[0].snippet == "x" * 2000


def test_search_web_empty_content_fallback():
    mock_response = {
        "results": [
            {
                "title": "No Content Page",
                "url": "https://example.com/empty",
                "content": "",
            }
        ]
    }

    with patch("riplex.services.search.client.search", return_value=mock_response):
        sources = search_web("Empty content test")
        assert len(sources) == 1
        assert sources[0].snippet == "No content available"


def test_search_web_propagates_client_error():
    with patch("riplex.services.search.client.search", side_effect=RuntimeError("API error")):
        with pytest.raises(RuntimeError, match="API error"):
            search_web("Trigger error")
