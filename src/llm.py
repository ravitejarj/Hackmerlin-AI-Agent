import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com/v1/chat/completions"


def ask_llm(prompt: str, temperature: float = 0.3, max_tokens: int = 100) -> str:
    if not DEEPSEEK_API_KEY:
        return "LLM error: missing DEEPSEEK_API_KEY"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are HackMerlin solver. Respond concisely."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        resp = requests.post(BASE_URL, headers=headers, json=payload, timeout=15)
        if resp.status_code == 401:
            return "LLM error: Unauthorized (check DEEPSEEK_API_KEY)"
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"LLM error: {e}"
