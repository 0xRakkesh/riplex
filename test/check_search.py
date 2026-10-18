
from riplex.services.search import search_web

sources = search_web("What is retrieval augmented generation?")

for source in sources:
    print(f"\nTitle: {source.title}")
    print(f"URL: {source.url}")
    print(f"Snippet: {source.snippet[:200]}")
