
import pytest
from pydantic import ValidationError

from riplex.schemas.research import RequestResearch, Source, ResearchReport

# RequestResearch tests

def test_valid_question():
    request = RequestResearch(
        question="What are AI agents?"
    )

    assert request.question == "What are AI agents?"


def test_empty_question():
    with pytest.raises(ValidationError):
        RequestResearch(question="")


def test_question_exceeds_max_length():
    with pytest.raises(ValidationError):
        RequestResearch(question="a" * 501)


def test_question_at_max_length():
    request = RequestResearch(question="a" * 500)

    assert len(request.question) == 500


def test_question_with_whitespace():
    request = RequestResearch(question="  What are AI agents?  ")

    assert request.question == "  What are AI agents?  "

# Source tests

def test_valid_source():
    source = Source(
        title="AI Agents Explained",
        url="https://example.com/ai-agents",
        snippet="An introduction to AI agents.",
        publication_date=None,
    )

    assert source.title == "AI Agents Explained"
    assert str(source.url) == "https://example.com/ai-agents"
    assert source.publication_date is None


def test_source_rejects_empty_title():
    with pytest.raises(ValidationError):
        Source(
            title="",
            url="https://example.com",
            snippet="Example source",
        )


def test_source_rejects_invalid_url():
    with pytest.raises(ValidationError):
        Source(
            title="Example",
            url="not-a-valid-url",
            snippet="Example source",
        )


def test_source_rejects_oversized_snippet():
    with pytest.raises(ValidationError):
        Source(
            title="Example",
            url="https://example.com",
            snippet="a" * 2001,
        )


def test_source_allows_missing_publication_date():
    source = Source(
        title="Example",
        url="https://example.com",
        snippet="Example source",
    )

    assert source.publication_date is None

# ResearchReport tests

def test_valid_research_report():
    source = Source(
        title="AI Agents Explained",
        url="https://example.com/ai-agents",
        snippet="An introduction to AI agents.",
    )

    report = ResearchReport(
        question="What are AI agents?",
        answer="AI agents can use tools to complete tasks.",
        sources=[source],
    )

    assert report.question == "What are AI agents?"
    assert report.answer == "AI agents can use tools to complete tasks."
    assert len(report.sources) == 1
    assert report.sources[0].title == "AI Agents Explained"


def test_research_report_rejects_invalid_source():
    with pytest.raises(ValidationError):
        ResearchReport(
            question="What are AI agents?",
            answer="An explanation.",
            sources=[
                {
                    "title": "Example",
                    "url": "invalid-url",
                    "snippet": "Example source",
                }
            ],
        )


def test_research_report_allows_empty_sources():
    report = ResearchReport(
        question="What are AI agents?",
        answer="Insufficient evidence was found.",
        sources=[],
    )

    assert report.sources == []
