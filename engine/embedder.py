"""
Thin wrapper around the Gemini embedding API.

Keeping this in its own module means that if Google changes the SDK,
or you swap models later, you only ever touch this one file - nothing
else in the pipeline needs to know how embedding actually happens.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from . import config

load_dotenv()
_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def embed_text(text: str, task_type: str = config.TASK_TYPE_DOCUMENT) -> list[float]:
    """
    Turn a piece of text into its embedding vector.

    task_type should be:
    - config.TASK_TYPE_DOCUMENT  when embedding content you're indexing
    - config.TASK_TYPE_QUERY     when embedding a user's question
    """
    response = _client.models.embed_content(
        model=config.EMBEDDING_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type=task_type),
    )
    return response.embeddings[0].values