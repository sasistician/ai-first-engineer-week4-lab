"""Tests for the Week 4 web-search MCP tool.

EVBot's test suite avoids mocking in favor of real-but-isolated instances
(e.g. an ephemeral local chromadb per test). There's no local equivalent
for a live web search API, so this suite mocks the DDGS client directly —
the one deliberate exception to that convention, worth noting if you're
comparing this repo's tests to EVBot's.
"""

from unittest.mock import patch

from server import search_web


def test_search_web_returns_normalized_results():
    fake_results = [
        {
            "title": "Rivian R1S Insurance Guide",
            "href": "https://example.com/r1s-insurance",
            "body": "Average annual premium...",
        }
    ]
    with patch("server.DDGS") as mock_ddgs_cls:
        mock_ddgs_cls.return_value.__enter__.return_value.text.return_value = fake_results
        results = search_web("2026 Rivian R1S insurance cost")

    assert results == [
        {
            "title": "Rivian R1S Insurance Guide",
            "url": "https://example.com/r1s-insurance",
            "snippet": "Average annual premium...",
        }
    ]


def test_search_web_clamps_max_results():
    with patch("server.DDGS") as mock_ddgs_cls:
        mock_instance = mock_ddgs_cls.return_value.__enter__.return_value
        mock_instance.text.return_value = []
        search_web("test query", max_results=50)

    mock_instance.text.assert_called_once_with("test query", max_results=10)


def test_search_web_handles_missing_fields_gracefully():
    with patch("server.DDGS") as mock_ddgs_cls:
        mock_ddgs_cls.return_value.__enter__.return_value.text.return_value = [{}]
        results = search_web("edge case query")

    assert results == [{"title": "", "url": "", "snippet": ""}]
