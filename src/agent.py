import os
from src.game_connector import ask_merlin
from src.config import COOKIES

LOG_DIR = "logs"
LEVEL_PROMPT_LOG = os.path.join(LOG_DIR, "level_prompt_log.txt")

os.makedirs(LOG_DIR, exist_ok=True)

def reset_level_prompt_log():
    with open(LEVEL_PROMPT_LOG, "w", encoding="utf-8") as f:
        f.write("")

def save_level_prompt_log(question: str, answer: str):
    with open(LEVEL_PROMPT_LOG, "a", encoding="utf-8") as f:
        f.write(f"Q: {question}\nA: {answer}\n---\n")

def agent_ask(question: str, cookies: dict = None) -> str:
    if cookies is None:
        cookies = COOKIES
    answer = ask_merlin(question, cookies)
    save_level_prompt_log(question, answer)
    return answer
