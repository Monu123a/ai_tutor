from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from rag import extract_pdf_text, chunk_text, create_embeddings, search_chunks
from llm import generate_answer
from image_search import find_best_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

STORE = {}

class ChatBody(BaseModel):
    topicId: str
    question: str

@app.get("/")
def health():
    return {"status": "ok", "message": "RAG AI Tutor API is running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    topic_id = str(uuid.uuid4())
    path = f"uploads/{topic_id}_{file.filename}"

    with open(path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_pdf_text(path)
        chunks = chunk_text(text)
        index = create_embeddings(chunks)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process PDF: {str(e)}")

    STORE[topic_id] = {
        "chunks": chunks,
        "index": index,
        "history": []
    }

    return {"topicId": topic_id}

@app.post("/chat")
def chat(data: ChatBody):
    if data.topicId not in STORE:
        raise HTTPException(status_code=404, detail="Topic not found. Please upload a PDF first.")

    topic = STORE[data.topicId]

    sources = search_chunks(
        data.question,
        topic["chunks"],
        topic["index"]
    )

    context = "\n".join(sources)

    try:
        answer = generate_answer(
            data.question,
            context,
            topic["history"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM error: {str(e)}")

    topic["history"].append({
        "role":"user",
        "content":data.question
    })

    topic["history"].append({
        "role":"assistant",
        "content":answer
    })

    image = find_best_image(data.question)

    return {
        "answer": answer,
        "sources": sources,
        "image": image
    }

@app.get("/images/{topicId}")
def get_images(topicId: str):
    return {"message":"Images linked dynamically"}