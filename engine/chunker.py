# GLORY BE TO GOD,
# CHUNKER - Full Pipeline
# by Israel Mafabi Emmanuel

"""
Splits extracted text into chunks ready for embedding.

Two strategies live here:
- chunk_prose:  generic paragraph-based chunking, for narrative
                documents like a policy doc.
- chunk_faq:    one chunk per Q&A pair, for FAQ-style documents -
                this keeps each question and its answer together,
                which matches how a user will actually ask things.

choose_chunks() picks a strategy based on the file name, so main.py
never needs to know the details. Add a new "chunk_xyz" function here
and a new branch in choose_chunks() whenever a new document type shows up.
"""

import re
from . import config

# Matches numbered section titles, e.g. "9. Policy Review and Compliance"
_NUMBERED_HEADING = re.compile(r"^\d+\.\s+[A-Z]")


def _looks_like_heading(paragraph: str) -> bool:
    """
    Heuristic for 'this line starts a new section, don't merge it into
    the previous chunk': either a numbered title like '9. Policy Review
    and Compliance', or a short line ending in a colon or nothing at all
    like 'Acknowledgment:' or 'Equipment and Expenses' (as opposed to a
    short line ending in '.', ';', or ')' - which is just a short sentence).
    """
    if _NUMBERED_HEADING.match(paragraph):
        return True
    return len(paragraph) < 60 and not paragraph.endswith((".", ";", ")"))


def _merge_short_chunks(chunks: list[str], min_chars: int = config.MIN_CHUNK_CHARS) -> list[str]:
    """
    Merge any chunk too short to carry real information (e.g. a lone
    document title isolated because the line right after it was also
    a heading) forward into the next chunk - or backward into the
    previous one, if it's the last chunk in the list.
    """
    if not chunks:
        return chunks

    merged = []
    carry = ""

    for chunk in chunks:
        combined = f"{carry}\n{chunk}".strip() if carry else chunk
        if len(combined) < min_chars:
            carry = combined  # still too short, hold and try adding the next chunk
        else:
            merged.append(combined)
            carry = ""

    if carry:  # leftover short piece at the very end - attach to the last real chunk
        if merged:
            merged[-1] = f"{merged[-1]}\n{carry}".strip()
        else:
            merged.append(carry)

    return merged


def chunk_prose(text: str, max_chars: int = config.MAX_CHUNK_CHARS) -> list[str]:
    """
    Group paragraphs into chunks up to max_chars each - but always start
    a new chunk when a heading is hit, so one chunk never blends two
    different policy sections together (e.g. overtime rules bleeding
    into the acknowledgment clause just because both fit under 1000 chars).
    Short leftover chunks (like an isolated title) get merged afterward.
    """
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        starts_new_section = _looks_like_heading(paragraph)
        too_long = len(current_chunk) + len(paragraph) + 1 > max_chars

        if current_chunk and (starts_new_section or too_long):
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
        else:
            current_chunk = f"{current_chunk}\n{paragraph}".strip()

    if current_chunk:
        chunks.append(current_chunk.strip())

    return _merge_short_chunks(chunks)


def chunk_faq(text: str) -> list[str]:
    """Split text into one chunk per Q&A pair, using 'Q:' as the marker."""
    raw_sections = text.split(config.FAQ_MARKER)

    chunks = []
    for section in raw_sections[1:]:  # index 0 is header text before the first "Q:"
        chunk = f"{config.FAQ_MARKER}{section}".strip()
        if chunk:
            chunks.append(chunk)

    return chunks


def choose_chunks(text: str, file_name: str) -> list[str]:
    """Pick a chunking strategy based on the source file name."""
    if "faq" in file_name.lower():
        return chunk_faq(text)
    return chunk_prose(text)