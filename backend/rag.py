import fitz
import faiss
import numpy as np
import requests
import os

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

def extract_api_vector(text):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables!")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={key}"
    payload = {
        "model": "models/text-embedding-004",
        "content": {"parts": [{"text": text[:2000]}]} # Cap at 2k chars to be safe
    }
    r = requests.post(url, json=payload, timeout=10)
    
    if r.status_code != 200:
        print("Embed Error:", r.text)
        return np.zeros(768).astype("float32")
        
    data = r.json()
    return np.array(data["embedding"]["values"]).astype("float32")

def create_embeddings(chunks):
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is missing from environment variables!")
        
    # Batch request for speed and efficiency
    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:batchEmbedContents?key={key}"
    payload = {
        "requests": [{"model": "models/text-embedding-004", "content": {"parts": [{"text": c[:2000]}]}} for c in chunks]
    }
    
    r = requests.post(url, json=payload)
    if r.status_code != 200:
        print("Batch Embed Error:", r.text)
        arr = np.zeros((len(chunks), 768)).astype("float32")
    else:
        data = r.json()
        vectors = [item["values"] for item in data.get("embeddings", [])]
        arr = np.array(vectors).astype("float32")

    index = faiss.IndexFlatL2(arr.shape[1])
    index.add(arr)

    return index

def search_chunks(question, chunks, index, k=4):
    q = extract_api_vector(question)
    q = np.array([q]).astype("float32")

    distances, ids = index.search(q, k)

    results = []
    for i in ids[0]:
        if i < len(chunks):
            results.append(chunks[i])

    return results

def embed_text(text):
    # Used purely by image_search.py for json metadata vectors
    return extract_api_vector(text)
