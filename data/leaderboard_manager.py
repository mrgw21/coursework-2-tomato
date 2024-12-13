import json
import os
from datetime import datetime


class LeaderboardManager:
    def __init__(self, filepath):
        # Ensure filepath is resolved relative to the project root
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.filepath = os.path.join(base_dir, filepath)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as file:
                json.dump({}, file)

    def get_leaderboard(self, level):
        with open(self.filepath, "r") as file:
            data = json.load(file)
        return data.get(level, [])

    def update_leaderboard(self, level, score):
        leaderboard = self.get_leaderboard(level)
        if len(leaderboard) >= 10 and score <= leaderboard[-1]["score"]:
            return False
        new_entry = {
            "score": score,
            "timestamp": datetime.now().strftime("%H:%M %d-%m-%Y"),
        }
        leaderboard.append(new_entry)

        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
        self._save_to_file(level, leaderboard)
        return True

    def _save_to_file(self, level, leaderboard):
        with open(self.filepath, "r") as file:
            data = json.load(file)

        data[level] = leaderboard

        with open(self.filepath, "w") as file:
            json.dump(data, file, indent=4)