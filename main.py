import sys
from src.solver import solve_with_llm as run_solver
from src.submitter import submit_password
from src.levels import load_levels, save_level
from src.config import COOKIES

def main():
    levels = load_levels()
    current_level = levels.get("currentLevel", 1)
    print(f"\n=== HackMerlin (Level {current_level}) ===")

    print("1) Enter password")
    print("2) Auto-solver")
    print("3) Exit")

    choice = input("Choose: ").strip()

    if choice == "1":
        pwd = input("Password: ").strip()
        if 5 <= len(pwd) <= 7:
            result = submit_password(pwd)
            if result:
                next_level = current_level + 1
                save_level(current_level, pwd, next_level)
        else:
            print("Must be 5–7 letters.")

    elif choice == "2":
        run_solver()

    elif choice == "3":
        sys.exit(0)

if __name__ == "__main__":
    main()
