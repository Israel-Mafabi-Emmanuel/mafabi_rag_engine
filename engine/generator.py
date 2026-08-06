"""
Generator module to interface with Gemini for generating conversational answers based on retrieved context.
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from . import config

load_dotenv()
_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

GENERATION_MODEL = "gemini-3.5-flash"

def generate_answer(question: str, chunks: list[str]) -> str:
    """
    Generates a natural language answer from Gemini based on the provided text chunks.
    """
    if not chunks:
        return "I don't have information about that in the current documents."

    # Build the prompt
    context_text = "\n\n---\n\n".join(chunks)
    
    prompt = f"""{config.ASSISTANT_PERSONA} Use the following document context to answer the user's question. 
    If the answer is not clearly present in the context, politely state that you do not have that information.
    Do not hallucinate or use outside knowledge.

    Context:
    {context_text}

    User Question:
    {question}
    """

    response = _client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2, # Keep it grounded
        )
    )
    
    return response.text
