"""
Retrieval - finds which stored chunks best match a user's question.

This module doesn't generate an answer yet - it just tells you which
chunks (and from which source file) are the best matches, with a
similarity score. Wiring those chunks into a Gemini generate() call
for a full natural-language answer is the very next step after this.
"""

import math
from . import config, embedder, vector_store


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """How similar two vectors are: 1 = identical direction, 0 = unrelated, -1 = opposite."""
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    magnitude_a = math.sqrt(sum(a * a for a in vec_a))
    magnitude_b = math.sqrt(sum(b * b for b in vec_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    return dot_product / (magnitude_a * magnitude_b)


def search(question: str, top_k: int = 3) -> list[dict]:
    """
    Embed the question, compare it against every stored chunk, and
    return the top_k best matches, each tagged with a similarity score.
    """
    records = vector_store.load_records()
    if not records:
        print(f"No embeddings found in {config.EMBEDDINGS_FILE} - run main.py first.")
        return []

    query_vector = embedder.embed_text(question, task_type=config.TASK_TYPE_QUERY)

    scored_records = []
    for record in records:
        score = cosine_similarity(query_vector, record["embedding"])
        scored_records.append({**record, "score": score})

    scored_records.sort(key=lambda r: r["score"], reverse=True)
    return scored_records[:top_k]