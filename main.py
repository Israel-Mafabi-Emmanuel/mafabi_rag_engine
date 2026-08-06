# GLORY BE TO GOD,
# EMBEDDING ENGINE - full pipeline,
# By Israel Mafabi Emmanuel
#
# Pipeline: PDF -> text -> chunks -> embeddings -> JSON store
#
# Setup:
#   1. Drop your PDFs into documents/pdf/
#   2. pip install pdfplumber google-genai python-dotenv
#   3. Make sure .env has GOOGLE_API_KEY=your_key_here
#   4. Run: python main.py
#
# Output:
#   - documents/txt/  gets one .txt file per PDF (for you to sanity-check)
#   - storage/embeddings.json  gets one record per chunk, ready for search

from engine import config, pdf_extractor, chunker, embedder, vector_store


def build_embeddings() -> None:
    txt_paths = pdf_extractor.extract_all_pdfs()

    if not txt_paths:
        print(f"No PDFs found in {config.PDF_DIR} - add some and run again.")
        return

    records = []
    for txt_path in txt_paths:
        text = txt_path.read_text(encoding="utf-8")
        chunks = chunker.choose_chunks(text, file_name=txt_path.name)

        for i, chunk_text in enumerate(chunks):
            vector = embedder.embed_text(chunk_text, task_type=config.TASK_TYPE_DOCUMENT)
            records.append({
                "source_file": txt_path.stem,
                "chunk_index": i,
                "chunk_text": chunk_text,
                "embedding": vector,
            })
            print(f"  embedded chunk {i} from {txt_path.stem}")

    vector_store.save_records(records)


if __name__ == "__main__":
    build_embeddings()