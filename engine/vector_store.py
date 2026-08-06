"""
Handles saving and loading embedding records to a local JSON file.

This is our POC vector store. When the project outgrows a flat JSON
file (more documents, need for persistence across a real server, etc.),
swap this module out for ChromaDB - nothing else in the pipeline
needs to change, since main.py only ever calls save_records/load_records.
"""

import json
from . import config


def save_records(records: list[dict]) -> None:
    """Write all embedding records to the JSON store, overwriting any existing file."""
    config.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    with open(config.EMBEDDINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(records)} records -> {config.EMBEDDINGS_FILE}")


def load_records() -> list[dict]:
    """Read back the stored embedding records, or return an empty list if none exist yet."""
    if not config.EMBEDDINGS_FILE.exists():
        return []
    with open(config.EMBEDDINGS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)