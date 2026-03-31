from app.pipeline.rag_pipeline import run_pipeline
from app.retrieval.web_search import search
from app.llm.groq_client import get_llm
from app.config import GROQ_API_KEY
query = input("Ask: ")

result = run_pipeline(query)

print("\nAnswer:\n", result["answer"])

print("\nSources:")
for i, s in enumerate(result["sources"]):
    print(f"[{i+1}] {s['url']}")