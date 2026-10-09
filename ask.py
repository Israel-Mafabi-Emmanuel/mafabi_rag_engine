# GLORY BE TO GOD,
# Interactive retrieval check - ask a question, see which stored
# chunks the engine thinks are the best match, and how confident it is.
#
# Run: python ask.py

from engine import config, search, generator


def main():
    question = input("Ask Aria a question: ")
    results = search.search(question, top_k=config.DEFAULT_TOP_K)

    if not results or results[0]["score"] < config.MIN_RELEVANCE_SCORE:
        print("\nAria: I don't have information about that in the current documents.")
        return

    for rank, result in enumerate(results, start=1):
        print(f"\n#{rank}  score={result['score']:.4f}  source={result['source_file']}")
        
    print("\nAria is generating answer...")
    chunks = [r["chunk_text"] for r in results]
    answer = generator.generate_answer(question, chunks)
    
    print("\n--- Aria's Answer ---")
    print(answer)
    print("----------------------")


if __name__ == "__main__":
    main()