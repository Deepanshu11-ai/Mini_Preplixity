from app.retrieval.web_search import search
from app.llm.groq_client import get_llm
from app.pipeline.decision import decide
from app.memory.chat_memory import add_to_memory, get_memory

llm = get_llm()

def run_pipeline(query: str):
    # 🧠 get past conversation
    memory = get_memory()

    # 🧠 decide mode
    decision = decide(query)

    # =========================
    # 🧠 NO SEARCH MODE
    # =========================
    if "NO_SEARCH" in decision:
        prompt = f"""
Conversation so far:
{memory}

User question:
{query}

Answer clearly and concisely.
"""
        response = llm.invoke(prompt)

        add_to_memory(query, response.content)

        return {
            "answer": response.content,
            "sources": ["Internal Knowledge"]
        }

    # =========================
    # 🌐 SEARCH MODE
    # =========================
    if "SEARCH" in decision and "HYBRID" not in decision:
        results = search(query)

        if not results:
            return {
                "answer": "No relevant results found.",
                "sources": []
            }

        context = ""
        for i, r in enumerate(results[:3]):
            context += f"[{i+1}] {r['title']}\n{r['content']}\n{r['url']}\n\n"

        prompt = f"""
Conversation so far:
{memory}

Answer using ONLY the sources.

Rules:
- Be direct
- Use citations like [1], [2]
- If user asks for a number (e.g., top 2), follow exactly

Question:
{query}

Sources:
{context}
"""

        response = llm.invoke(prompt)

        add_to_memory(query, response.content)

        return {
            "answer": response.content,
            "sources": results[:3]
        }

    # =========================
    # 🔥 HYBRID MODE
    # =========================
    if "HYBRID" in decision:
        results = search(query)

        if not results:
            return {
                "answer": "No relevant results found.",
                "sources": []
            }

        context = ""
        for i, r in enumerate(results[:3]):
            context += f"[{i+1}] {r['title']}\n{r['content']}\n{r['url']}\n\n"

        prompt = f"""
Conversation so far:
{memory}

You are an intelligent assistant.

Answer in TWO parts:

1. Explanation (use your own knowledge)
2. Latest updates (use sources)

Rules:
- Clearly separate both parts
- Use citations like [1], [2] for latest info
- Be concise and clear

Question:
{query}

Sources:
{context}
"""

        response = llm.invoke(prompt)

        add_to_memory(query, response.content)

        return {
            "answer": response.content,
            "sources": results[:3]
        }

    # =========================
    # ⚠️ FALLBACK
    # =========================
    response = llm.invoke(query)

    add_to_memory(query, response.content)

    return {
        "answer": response.content,
        "sources": ["Internal Knowledge"]
    }