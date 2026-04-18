import fitz
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_pdf_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def create_embeddings(chunks):
    vectors = model.encode(chunks)
    arr = np.array(vectors).astype("float32")

    index = faiss.IndexFlatL2(arr.shape[1])
    index.add(arr)

    return index

def search_chunks(question, chunks, index, k=4):
    q = model.encode([question])
    q = np.array(q).astype("float32")

    distances, ids = index.search(q, k)

    results = []
    for i in ids[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return results

def embed_text(text):
    return model.encode([text])[0]
