# GLORY BE TO GOD,
# FRONTDESK ASSISTANT - FULL PIPELINE - API
# by Israel Mafabi Emmanuel

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import shutil
import os
from pathlib import Path

from engine import config, search, generator
import main as pipeline_main

app = FastAPI(title="FrontDesk Assistant API")

# Mount templates directory if it exists
templates_dir = Path("templates")
if templates_dir.exists():
    app.mount("/static", StaticFiles(directory="templates"), name="static")

class AskRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serves the simple HTML frontend for testing."""
    index_path = templates_dir / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>API is running. Please create templates/index.html to view the UI.</h1>"

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Accepts a PDF upload, saves it, and triggers the embedding pipeline."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    # Save the file
    save_path = config.PDF_DIR / file.filename
    try:
        with save_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
        
    # Trigger the pipeline (rebuilds embeddings for all PDFs including the new one)
    try:
        pipeline_main.build_embeddings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")
        
    return {"message": f"Successfully processed {file.filename} and updated embeddings."}

@app.post("/api/ask")
async def ask_question(request: AskRequest):
    """Answers a question based on the document embeddings."""
    results = search.search(request.question, top_k=3)
    
    # Check relevance
    if not results or results[0]["score"] < config.MIN_RELEVANCE_SCORE:
        return {
            "answer": "I don't have information about that in the current documents.",
            "sources": []
        }
        
    chunks = [r["chunk_text"] for r in results]
    sources = list(set([r["source_file"] for r in results]))
    
    # Generate conversational answer
    answer = generator.generate_answer(request.question, chunks)
    
    return {
        "answer": answer,
        "sources": sources
    }
