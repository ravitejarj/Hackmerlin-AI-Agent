import os
import re
from src.agent import agent_ask, LEVEL_PROMPT_LOG
from src.llm import ask_llm
from src.levels import load_levels

ANSWER_LOG = os.path.join("logs", "answer_log.txt")

def ask_merlin_batch(cookies: dict, questions: list[str]) -> None:
    for q in questions:
        ans = agent_ask(q, cookies)
        _ = ans  # logged automatically

def extract_explicit_passwords(text: str) -> list[str]:
    patterns = [
        r"password is [\"']?([A-Z]{5,7})[\"']?",
        r"password: [\"']?([A-Z]{5,7})[\"']?",
        r"full password is [\"']?([A-Z]{5,7})[\"']?",
        r"word you seek is [\"']?([A-Z]{5,7})[\"']?",
        r"the secret word is [\"']?([A-Z]{5,7})[\"']?",
    ]
    found = []
    for pat in patterns:
        matches = re.findall(pat, text, re.IGNORECASE)
        found.extend(matches)
    return list(dict.fromkeys([w.upper() for w in found]))

def read_prompt_log() -> str:
    try:
        with open(LEVEL_PROMPT_LOG, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""

def load_answer_log() -> list[str]:
    if os.path.exists(ANSWER_LOG):
        with open(ANSWER_LOG, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def extract_caps_from_log() -> str:
    return " ".join(re.findall(r"\b[A-Z]{5,7}\b", read_prompt_log()))

def deduce_candidates(num_words: int = 10) -> list[str]:
    conversation = read_prompt_log()
    previous_candidates = load_answer_log()
    caps_letters = extract_caps_from_log()

    explicit = extract_explicit_passwords(conversation)
    candidates = list(explicit)

    if not candidates:
        prompt = f"""
The password is ALWAYS between 5 and 7 letters long.

Clues from Merlin’s answers:
{conversation}

Uppercase hints:
{caps_letters or '(none)'}

Previous guesses:
{', '.join(previous_candidates) if previous_candidates else '(none)'}

Task:
- Generate {num_words} NEW candidate words not in the previous guesses.
- Each must be a valid English word, 5–7 letters long.
- Use the letter clues and uppercase hints to reconstruct.
- Correct small mistakes (like reversed letters or missing vowels).
- Output {num_words} unique words in FULL UPPERCASE, one per line.
"""
        raw = ask_llm(prompt).splitlines()
        for w in raw:
            w = w.strip().upper()
            if w and 5 <= len(w) <= 7 and w not in candidates and w not in previous_candidates:
                candidates.append(w)

    if candidates:
        os.makedirs("logs", exist_ok=True)
        with open(ANSWER_LOG, "a", encoding="utf-8") as f:
            for w in candidates:
                f.write(w + "\n")

        before = len(previous_candidates)
        after = before + len(candidates)
        batch_num = (before // 10) + 1
        print(f"🔮 Batch {batch_num} generated ({before+1}-{after} guesses)")

    return candidates
