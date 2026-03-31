from app.llm.groq_client import get_llm

llm = get_llm()

def decide(query: str):
    prompt = f"""
Decide how to answer the query.

Rules:
- If only general knowledge → NO_SEARCH
- If only latest info → SEARCH
- If both explanation + latest info → HYBRID

Return ONLY one word:
NO_SEARCH / SEARCH / HYBRID

Query:
{query}
"""
    response = llm.invoke(prompt)
    return response.content.strip()