import json
import os

SAVE_FILE_PATH = os.path.join("data", "saves/save_data.json")

def save_progress(data):
    os.makedirs(os.path.dirname(SAVE_FILE_PATH), exist_ok=True)
    with open(SAVE_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

def load_progress():
    try:
        with open(SAVE_FILE_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"level1_completed": False}