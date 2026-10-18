from tavily import TavilyClient
import pysbd
from riplex.core.config import TAVILY_API_KEY
from riplex.schemas.research import Source

client = TavilyClient(api_key=TAVILY_API_KEY)
segmenter = pysbd.Segmenter(language="en")

def search_web(query: str, num_results: int = 5) -> list[Source]:

    response = client.search(query,search_depth="basic",max_results=num_results)
    sources = []
    for results in response.get("results",[]):
            source = Source(
                title=results.get("title"),
                url=results.get("url"),
                snippet=(results.get("content") or "")[:10000],
                publication_date=results.get("publication_date"),
            )
            sources.append(source)
    return sources
    