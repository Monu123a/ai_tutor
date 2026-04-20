import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "image_data.json"), "r") as f:
    IMAGES = json.load(f)

image_texts = [img["title"] + " " + img["description"] + " " + " ".join(img["keywords"]) for img in IMAGES]
vectorizer = TfidfVectorizer(stop_words='english')
if image_texts:
    try:
        tfidf_matrix = vectorizer.fit_transform(image_texts)
    except ValueError:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(image_texts)
else:
    tfidf_matrix = None

def find_best_image(query):
    if tfidf_matrix is None:
        return None

    short_query = " ".join(query.split()[:50])
    q_vec = vectorizer.transform([short_query])
    
    scores = cosine_similarity(q_vec, tfidf_matrix)[0]
    best_idx = np.argmax(scores)
    best_score = scores[best_idx]
    
    if best_score > 0.1:
        return IMAGES[best_idx]
    return None