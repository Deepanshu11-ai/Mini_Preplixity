from tavily import TavilyClient
from app.config import TAVILY_API_KEY

tavily = TavilyClient(api_key=TAVILY_API_KEY)

def search(query: str):
    response = tavily.search(query=query, max_results=5)

    results = []

    for r in response.get("results", []):
        url = r.get("url", "")

        
        if "youtube.com" in url:
            continue

        results.append({
            "title": r.get("title", ""),
            "content": r.get("content", ""),
            "url": url
        })

    return results