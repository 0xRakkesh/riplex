from langchain.tools import tool
from riplex.services.search import search_web

@tool
def web_search(query: str) :
    """Search the internet for current facts, external evidence,
    niche information, or sources needed to answer a research question.
    Do not use for basic explanations or questions answerable reliably
    without external information."""
    return search_web(query)
