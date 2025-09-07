import requests
from src.config import COOKIES

BASE_URL = "https://hackmerlin.io/api/question"
HEADERS = {"Content-Type": "text/plain", "Accept": "*/*"}

def ask_merlin(question: str, cookies: dict = None) -> str:
    if cookies is None:
        cookies = COOKIES  # ✅ default from config
    try:
        resp = requests.post(
            BASE_URL,
            headers=HEADERS,
            cookies=cookies,
            data=question.encode("utf-8"),
            timeout=10
        )
        resp.raise_for_status()
        return resp.text.strip()
    except requests.RequestException as e:
        return f"Request error: {e}"
