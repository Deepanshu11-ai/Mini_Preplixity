from tavily import TavilyClient
from app.config import TAVILY_API_KEY

tavily=TavilyClient(
    api_key=TAVILY_API_KEY
)

def search(query:str):
    response=tavily.search(
        query=query,
        max_results=5,
        top_k=5
    )
    result=[]
    for r in response["results"]:
        result.append(
            {
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            }
        )
    return result