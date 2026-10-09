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
    
    prompt = f"""{config.ASSISTANT_PERSONA}

Context from documents:
{context_text}

User Question:
{question}

Response Guidelines:
1. Answer the question directly, warmly, and constructively based on the context above.
2. If the user asks about a policy or topic (such as work hours, equipment, or communication) that is discussed in the context, explain the relevant requirements, guidelines, and arrangements clearly.
3. If a specific metric or figure is not defined in the text, highlight what IS defined (e.g., Core Hours, manager-coordinated schedules) rather than starting with an apologetic disclaimer.
4. Only state that you don't have the information if the topic is genuinely absent from the context.
5. Use clean formatting (bullet points, bold highlights for hours, deadlines, or tools) for scannability.
6. Keep answers grounded strictly in the provided context—never hallucinate outside facts.
"""

    response = _client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2, # Keep it grounded
        )
    )
    
    return response.text
