import requests
from src.config import COOKIES

BASE_URL = "https://hackmerlin.io/api/submit"
HEADERS = {
    "Content-Type": "text/plain",
    "Accept": "*/*"
}

def submit_password(password: str, cookies: dict = None) -> dict:
    """
    Submit a password guess to HackMerlin API.
    Returns JSON with next level info or error.
    """
    if cookies is None:
        cookies = COOKIES

    try:
        resp = requests.post(
            BASE_URL,
            headers=HEADERS,
            cookies=cookies,
            data=password.strip(),
            timeout=10
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}
