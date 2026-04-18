import os
import requests
from dotenv import load_dotenv

# Load .env from parent directory (project root)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

API_KEY = os.getenv("GROQ_API_KEY")

def generate_answer(question, context, history=[]):
    if not API_KEY or API_KEY == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY is not set. Please add your Groq API key to the .env file."
        )

    chat_history = ""

    for item in history[-3:]:
        chat_history += f"{item['role']}: {item['content']}\n"

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

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role":"user","content":prompt}
        ]
    }

    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=body,
            headers=headers,
            timeout=30
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Groq API error ({r.status_code}): {r.text}")
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected Groq API response: {r.text}")