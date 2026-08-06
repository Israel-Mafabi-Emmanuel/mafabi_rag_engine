# Mafabi ML Engine & FrontDesk Assistant
A modular Retrieval-Augmented Generation (RAG) pipeline and API designed to ingest PDFs, embed their content, and provide intelligent conversational answers based on the text.

## The "Why"
Have you ever wanted a virtual assistant that can instantly recall and synthesize information from a large collection of your own documents? This project serves as an inspirational recipe for building your own knowledge-based AI. It solves the problem of searching through endless PDFs by extracting the text, chunking it into digestible pieces, mapping those chunks into vector embeddings using Google GenAI, and exposing an easy-to-use FastAPI backend for asking questions against your private data. Whether you're building a "FrontDesk" virtual receptionist or just experimenting with RAG pipelines, this is the perfect launchpad. 

## Tech Stack
- **Python 3.8+**
- **FastAPI** (for the REST API)
- **Google GenAI** (for vector embeddings and answer generation)
- **PDFPlumber** (for precise text extraction)
- **Scikit-learn, Numpy, Pandas** (data and math ops)

## Architecture / File Purposes
- **`main.py`**: The core embedding pipeline script. It orchestrates the process from reading PDFs to saving vectors.
- **`api.py`**: A FastAPI application that provides routes to upload new PDFs (`/api/upload`) and query the knowledge base (`/api/ask`).
- **`engine/`**: The brain of the project, containing modular scripts for extraction (`pdf_extractor.py`), chunking (`chunker.py`), embedding (`embedder.py`), vector storage (`vector_store.py`), and answer generation (`generator.py`).
- **`documents/pdf/`**: Drop your raw PDF files in this folder for ingestion.
- **`storage/`**: Contains the generated `embeddings.json` file which acts as our local vector database.

## Execution
Follow these recipe steps to get your own FrontDesk Assistant running:

1. **Clone & Set Up Environment**
   Create a conda environment from the provided file or use `pip`:
   ```bash
   conda env create -f environment.yml
   conda activate mafabi_ml_engine
   # Or install dependencies manually:
   pip install fastapi uvicorn pdfplumber google-genai python-dotenv
   ```

2. **Configure API Keys**
   Create a `.env` file in the root directory and add your Google GenAI API key:
   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Ingest Documents**
   Place any PDF files you want to query inside the `documents/pdf/` directory. Then, build the embeddings:
   ```bash
   python main.py
   ```

4. **Start the API Server**
   Spin up the FastAPI backend to interact with your data:
   ```bash
   uvicorn api:app --reload
   ```

---
**Glory to GOD**
*By Emmanuel Mafabi Israel, Mafabi Innovations*
