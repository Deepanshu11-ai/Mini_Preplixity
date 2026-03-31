from app.retrieval.web_search import search
from app.llm.groq_client import get_llm

llm = get_llm()

def run_pipeline(query: str):
    results = search(query)

    # safety check
    if not results:
        return {
            "answer": "No relevant results found.",
            "sources": []
        }

    # 🔥 limit context (top 3 only)
    context = ""
    for i, r in enumerate(results[:3]):
        context += f"[{i+1}] {r['title']}\n{r['content']}\n{r['url']}\n\n"

    # 🧠 improved prompt
    prompt = f"""
You are an AI news assistant.

Answer the user's question using ONLY the sources provided.

Rules:
- Give a direct answer (no vague language like "it seems")
- If user asks for "top 2", return EXACTLY 2 points
- Be concise and confident
- Use citations like [1], [2]
- Ignore irrelevant information

Question:
{query}

Sources:
{context}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": results[:3]
    }