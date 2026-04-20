import fitz
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(chunks)
    except ValueError:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(chunks)
    return (vectorizer, tfidf_matrix)

def search_chunks(question, chunks, index, k=4):
    vectorizer, tfidf_matrix = index
    q_vec = vectorizer.transform([question])
    scores = cosine_similarity(q_vec, tfidf_matrix)[0]
    
    best_indices = np.argsort(scores)[-k:][::-1]
    
    results = []
    for i in best_indices:
        if scores[i] > 0.05:
            results.append(chunks[i])
            
    if not results and len(chunks) > 0:
        results = [chunks[best_indices[0]]]
        
    return results[:k]
