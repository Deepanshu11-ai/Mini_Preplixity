from app.pipeline.rag_pipeline import run_pipeline

def main():
    print("🚀 Mini Perplexity AI (type 'exit' to quit)\n")

    while True:
        try:
            query = input("Ask: ").strip()

            # exit condition
            if query.lower() in ["exit", "quit"]:
                print("👋 Exiting... see you.")
                break

            # skip empty input
            if not query:
                continue

            result = run_pipeline(query)

            # 🧠 print answer
            print("\nAnswer:\n")
            print(result["answer"])

            # 🌐 print sources
            print("\nSources:")
            for i, s in enumerate(result["sources"]):
                if isinstance(s, dict):
                    print(f"[{i+1}] {s.get('url', '')}")
                else:
                    print(f"[{i+1}] {s}")

            print("\n" + "-"*50 + "\n")

        except KeyboardInterrupt:
            print("\n👋 Interrupted. Bye.")
            break

        except Exception as e:
            print("\n⚠️ Error occurred:", str(e))
            print("Continuing...\n")


if __name__ == "__main__":
    main()