import os
from src.merlin_solver import ask_merlin_batch, deduce_candidates, ANSWER_LOG
from src.submitter import submit_password
from src.levels import load_levels, save_level
from src.agent import reset_level_prompt_log
from src.instructions import QUESTION_INSTRUCTIONS
from src.config import COOKIES
from src.llm import ask_llm

LEVEL_QUESTION_LIMITS = {1: 10, 2: 20, 3: 20, 4: 30, 5: 30, 6: 30}

def count_guesses() -> int:
    if os.path.exists(ANSWER_LOG):
        with open(ANSWER_LOG, "r", encoding="utf-8") as f:
            return len([line.strip() for line in f if line.strip()])
    return 0

def solve_with_llm(cookies: dict = None):
    if cookies is None:
        cookies = COOKIES

    while True:
        levels = load_levels()
        current_level = levels.get("currentLevel", 1)
        max_questions = LEVEL_QUESTION_LIMITS.get(current_level, 20)

        print(f"\n⚡ Solving Level {current_level} | Max {max_questions} Qs")

        solved = False
        total_questions = 0

        while not solved:
            # Step 1: Ask 10 questions if limit not reached
            if total_questions < max_questions:
                q_prompt = QUESTION_INSTRUCTIONS["level_1"] if current_level == 1 else QUESTION_INSTRUCTIONS["level_2_6"]

                if os.path.exists("logs/level_prompt_log.txt"):
                    with open("logs/level_prompt_log.txt", "r", encoding="utf-8") as f:
                        conversation = f.read()
                    q_prompt += f"\nAlready asked (Q/A log):\n{conversation}\n"

                q_prompt += "\nGenerate exactly 10 NEW unique questions.\n"

                new_qs = [q.strip() for q in ask_llm(q_prompt).splitlines() if q.strip()]
                new_qs = new_qs[:10]

                if new_qs:
                    total_questions += len(new_qs)
                    print(f"📝 Asked {total_questions}/{max_questions} questions")
                    ask_merlin_batch(cookies, new_qs)
                else:
                    print("⚠️ No new questions.")
            else:
                print(f"⚠️ Reached Q limit ({max_questions}) → candidates only.")

            # Step 2: Candidate testing (batch-based, printing in merlin_solver)
            while not solved:
                candidates = deduce_candidates(num_words=10)
                if not candidates:
                    print("⚠️ No new candidates.")
                    break

                for guess in candidates:
                    if not (5 <= len(guess) <= 7):
                        continue
                    result = submit_password(guess, cookies)
                    if "error" in result:
                        continue
                    if result.get("currentLevel") and "finishedMessage" in result:
                        new_level = result["currentLevel"]
                        print(f"🎉 SOLVED L{current_level} → {guess}")
                        print(f"➡️ Next: Level {new_level}/{result['maxLevel']}")
                        print(f"📜 {result['finishedMessage']}")
                        save_level(current_level, guess, new_level)
                        reset_level_prompt_log()
                        if os.path.exists(ANSWER_LOG):
                            os.remove(ANSWER_LOG)
                        solved = True
                        break

                if solved:
                    break

                tried = count_guesses()
                print(f"⚡ Total guesses tried: {tried}")

                if tried % 50 == 0:
                    if total_questions < max_questions:
                        print("🔄 Asking next 10 questions...\n")
                        break
                    else:
                        print("🔁 Q limit reached → keep generating candidates.")
                        continue
