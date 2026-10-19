from unittest.mock import patch
from riplex.services.tools import web_search
from riplex.schemas.research import Source


def test_web_search_tool_metadata():
    """Verify tool metadata and description."""
    assert web_search.name == "web_search"
    assert "Search the internet" in web_search.description


def test_web_search_tool_invoke():
    """Verify invoking the tool calls search_web and returns sources."""
    mock_sources = [
        Source(
            title="LangChain Guide",
            url="https://example.com/langchain",
            snippet="Guide on LangChain tools.",
            publication_date="2026-01-01",
        )
    ]

    with patch("riplex.services.tools.search_web", return_value=mock_sources) as mock_search:
        result = web_search.invoke({"query": "langchain tools"})
        mock_search.assert_called_once_with("langchain tools")
        assert result == mock_sources
        assert len(result) == 1
        assert result[0].title == "LangChain Guide"


def test_web_search_tool_direct_call():
    """Verify calling the tool directly as a function."""
    mock_sources = []
    with patch("riplex.services.tools.search_web", return_value=mock_sources) as mock_search:
        result = web_search.run("test query")
        mock_search.assert_called_once_with("test query")
        assert result == mock_sources
