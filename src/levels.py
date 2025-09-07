import json
from pathlib import Path
from typing import Any, Dict

LEVELS_FILE = Path("levels.json")

def load_levels() -> Dict[str, Any]:
    if LEVELS_FILE.exists():
        try:
            with open(LEVELS_FILE, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)
                if not data:
                    return {"currentLevel": 1}
                return data
        except Exception:
            return {"currentLevel": 1}
    return {"currentLevel": 1}

def save_level(level: int, password: str, next_level: int) -> None:
    data: Dict[str, Any] = load_levels()
    data[f"level_{level}"] = password
    data["currentLevel"] = next_level

    with open(LEVELS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"💾 Saved Level {level} → {password}, next level = {next_level}")
