# Azure OpenAI integration logic
import os
import requests

ZEMINI_API_KEY = os.getenv("ZEMINI_API_KEY")
ZEMINI_API_URL = os.getenv("ZEMINI_API_URL")

headers = {
    "Authorization": f"Bearer {ZEMINI_API_KEY}",
    "Content-Type": "application/json"
}

def generate_ai_response(prompt: str) -> str:
    payload = {"prompt": prompt, "max_tokens": 150}
    response = requests.post(f"{ZEMINI_API_URL}/generate", headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("text", "")
