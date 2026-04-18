# RAG AI Tutor with Interactive Images

A full-stack AI Tutor application designed to teach concepts from any uploaded PDF chapter by dynamically responding with context-grounded text and perfectly matched scientific diagrams.

## 🚀 Quick Start (Local Run Steps)

### 1. Start the Backend (FastAPI)
```bash
# Navigate to the project root
cd backend

# Create and activate a virtual environment (if not already done)
# python3 -m venv venv
source ../venv/bin/activate

# Install dependencies  
pip install -r ../requirements.txt

# Start the uvicorn server
python -m uvicorn main:app --reload
```
*The backend will now be running on `http://localhost:8000`*

### 2. Start the Frontend (Vite + React)
```bash
# In a new terminal, navigate to the frontend directory
cd frontend-react

# Install packages
npm install

# Run the Vite dev server
npm run dev
```
*The React app will be available on `http://localhost:5173`*

---

## 🧠 Architecture Overview

### 1. RAG Pipeline Implementation
The text pipeline extracts specific information from large context chunks to ensure the LLM generates accurate and completely grounded answers:

1. **Extraction & Chunking:** When a user uploads a PDF, `fitz` (PyMuPDF) extracts all text. The text is broken down into 500-character chunks with a 100-character overlap to preserve context continuity between passages.
2. **Embeddings:** Each textual chunk is encoded into dense vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
3. **Storage & Retrieval:** The embeddings are loaded into a local in-memory `FAISS` index (L2 distance). When the user asks a question, this exact same model embeds the user's query, compares the vector distances, and instantly pulls the Top `K=4` most relevant text chunks.
4. **Generation:** The context chunks and the chat history are fed directly into a localized prompt tailored for an AI Tutor.

### 2. Image Retrieval Logic
Rather than generically linking images, the app natively performs semantic vector-similarity matching for visual assets:

1. **Metadata Definition:** The application utilizes a hardcoded JSON graph (`backend/image_data.json`) storing 4 high-quality pre-existing images (Compression/Rarefaction, Reflective Echo, School Bell Vibration, Musical Instruments). Each entry maps the `filename` alongside descriptive `titles`, `descriptions`, and extensive `keywords`.
2. **Context Embedding:** On system startup, the descriptions of these specific images are fully embedded using the `MiniLM` standard embedding space.
3. **Dynamic Matching:** Upon receiving an answer request, the system slices the user's query to reduce noise and embeds it. A `Cosine Similarity` computation scores the user's query vector against all available image descriptive vectors. 
4. **Delivery:** The backend isolates the single highest-scoring image metadata (ignoring irrelevant noise via a custom `0.15` floor threshold) and returns the JSON payload alongside the text, allowing the React frontend to display the static asset identically.

### 3. LLM Prompts Used
The specific system prompt controlling the conversational model operates directly under stringent context confines. If a relevant answer is strictly missing, it refuses to hallucinate:

```python
prompt = f"""
You are an AI Tutor.

Use ONLY the provided context.
If answer is missing, say:
'I could not find that in the uploaded chapter.'

Previous Chat:
{chat_history}

Context:
{context}

Question:
{question}

Answer clearly for a student.
"""
```

## 🛠 Tech Stack
- **Frontend**: React (Vite), pure modern CSS (Glassmorphism, Dark UI)
- **Backend**: FastAPI (Python), `uvicorn`
- **AI Models**: Groq Cloud (`llama-3.1-8b-instant`), HuggingFace (`all-MiniLM-L6-v2`)
- **Libaries**: `FAISS`, `sentence-transformers`, `PyMuPDF`, `axios`
