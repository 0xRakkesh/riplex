from unittest.mock import patch
import pytest
from pydantic import ValidationError
from riplex.main import app, health, research
from riplex.schemas.research import RequestResearch


def test_app_metadata():
    """Verify FastAPI application title and configuration."""
    assert app.title == "Research Agent APIs"


def test_health_endpoint():
    """Verify health endpoint returns status ok."""
    response = health()
    assert response == {"status": "ok"}


def test_research_endpoint_success():
    """Verify research endpoint calls run_agent and returns question and answer."""
    req = RequestResearch(question="What is transfer learning?")
    with patch("riplex.main.run_agent", return_value="Transfer learning is reusing a pre-trained model.") as mock_agent:
        result = research(req)

        mock_agent.assert_called_once_with("What is transfer learning?")
        assert result == {
            "question": "What is transfer learning?",
            "answer": "Transfer learning is reusing a pre-trained model.",
        }


def test_research_endpoint_rejects_empty_question():
    """Verify RequestResearch validates that empty questions are rejected."""
    with pytest.raises(ValidationError):
        RequestResearch(question="")


def test_research_endpoint_rejects_oversized_question():
    """Verify RequestResearch validates that questions over 500 characters are rejected."""
    with pytest.raises(ValidationError):
        RequestResearch(question="q" * 501)


def test_openapi_schema_routes():
    """Verify OpenAPI schema includes /health and /research with proper methods."""
    schema = app.openapi()
    paths = schema.get("paths", {})

    assert "/health" in paths
    assert "get" in paths["/health"]

    assert "/research" in paths
    assert "post" in paths["/research"]


def test_app_routes_registered():
    """Verify routes are registered on the FastAPI app."""
    route_paths = {route.path: route for route in app.routes}

    assert "/health" in route_paths
    assert "/research" in route_paths
