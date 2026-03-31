from app.retrieval.web_search import search
from app.llm.groq_client import get_llm

llm = get_llm()

def run_pipeline(query: str):
    results = search(query)

    context = ""
    for i, r in enumerate(results):
        context += f"[{i+1}] {r['title']}\n{r['content']}\n{r['url']}\n\n"

    prompt = f"""
    Answer the question using ONLY the sources below.

    Question:
    {query}

    Sources:
    {context}

    Instructions:
    - Cite sources like [1], [2]
    - Be concise
    - If unsure, say you don't know
    """

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": results
    }