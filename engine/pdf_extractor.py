"""
Pulls raw text out of PDFs in documents/pdf and writes a matching .txt
file into documents/txt, so you can eyeball extraction quality before
it ever touches the embedding API.
"""

import pdfplumber
from pathlib import Path
from . import config


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Read a single PDF and return its full text as one string."""
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            pages_text.append(page_text)
    return "\n".join(pages_text)


def extract_all_pdfs() -> list[Path]:
    """
    Extract every PDF in documents/pdf, save each as a .txt file in
    documents/txt, and return the list of .txt file paths created.
    """
    config.TXT_DIR.mkdir(parents=True, exist_ok=True)
    txt_paths = []

    for pdf_path in sorted(config.PDF_DIR.glob("*.pdf")):
        text = extract_text_from_pdf(pdf_path)

        txt_path = config.TXT_DIR / f"{pdf_path.stem}.txt"
        # utf-8 explicitly, to avoid Windows' default codec mangling special characters
        txt_path.write_text(text, encoding="utf-8")

        txt_paths.append(txt_path)
        print(f"Extracted: {pdf_path.name} -> {txt_path.name}")

    return txt_paths