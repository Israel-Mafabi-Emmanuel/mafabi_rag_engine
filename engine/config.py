# GLORY BE TO GOD,
# CONFIGURATION FILE - Full Pipeline
# by Israel Mafabi Emmanuel

"""
Central configuration for the Mafabi Embedding Engine.
Change values here instead of hunting through every module.
"""

from pathlib import Path

# --- Project folders ---
BASE_DIR = Path(__file__).resolve().parent.parent  # mafabi_ml_engine/
PDF_DIR = BASE_DIR / "documents" / "pdf"
TXT_DIR = BASE_DIR / "documents" / "txt"
STORAGE_DIR = BASE_DIR / "storage"
EMBEDDINGS_FILE = STORAGE_DIR / "embeddings.json"

# --- Gemini embedding settings ---
# gemini-embedding-001 is used (not gemini-embedding-2) because this
# project is text-only and we need the task_type parameter, which
# gemini-embedding-001 supports directly.
EMBEDDING_MODEL = "gemini-embedding-001"
TASK_TYPE_DOCUMENT = "RETRIEVAL_DOCUMENT"  # used when embedding content we're indexing
TASK_TYPE_QUERY = "RETRIEVAL_QUERY"        # used when embedding a user's question

# --- Chunking settings ---
MAX_CHUNK_CHARS = 1000   # ceiling for a prose chunk before we split it
FAQ_MARKER = "Q:"        # what signals the start of a new FAQ chunk

# --- Relevance threshold ---
# Below this cosine similarity score, we treat the top match as "not
# actually relevant" rather than force-feeding a weak result forward.
# Calibrated from real tests: off-topic questions scored ~0.539, genuine
# matches scored 0.74-0.81. 0.6 sits safely between the two with margin
# on both sides - revisit this number as you run more real questions.
MIN_RELEVANCE_SCORE = 0.6

# A chunk shorter than this carries basically no retrievable information
# (e.g. a lone document title that got isolated by heading-boundary
# splitting) and gets merged into a neighboring chunk instead of being
# embedded and searched on its own.
MIN_CHUNK_CHARS = 40

# --- Retrieval depth ---
DEFAULT_TOP_K = 4

# --- Assistant Persona ---
# This is the "System Prompt" that tells the LLM who it is and how it should behave.
# By keeping it on the server, we prevent clients from overriding it.
#
# Language strategy: adaptive mirroring.
# The assistant detects and matches the user's language, tone, and style —
# formal, casual, Swahili, English, mixed — making conversations feel natural
# and relatable rather than rigid. The LLM's contextual understanding makes
# this far more accurate than any rule-based or pre-processing approach.
ASSISTANT_PERSONA = (
    "You are Aria, an intelligent, professional, and friendly FrontDesk assistant for Acme Corp. "
    "You provide clear, accurate, and constructive answers grounded in the provided company documents. "
    "Communicate naturally and concisely, without robotic disclaimers. "
    "Always mirror the user's language, tone, and style."
)