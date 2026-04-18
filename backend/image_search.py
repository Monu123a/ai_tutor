import json
import os
import numpy as np
from rag import embed_text

BASE = os.path.dirname(__file__)

with open(os.path.join(BASE, "image_data.json"), "r") as f:
    IMAGES = json.load(f)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_best_image(query):
    # Shorten the query to main keywords or just first 200 chars to avoid noise
    short_query = " ".join(query.split()[:50])
    q_vec = embed_text(short_query)

    best = None
    best_score = -1

    for img in IMAGES:
        # Construct a descriptive text combining metadata
        text = img["title"] + " " + img["description"] + " " + " ".join(img["keywords"])
        vec = embed_text(text)

        score = cosine(q_vec, vec)

        if score > best_score:
            best_score = score
            best = img

    # Only return an image if it has some minimum relevance, else None
    if best_score > 0.15:
        return best
    return None