import os
import subprocess
import requests

UPDATE_URL = "https://raw.githubusercontent.com/AftabJ09/rain-of-blocks-updates/main/version.txt"
LOCAL_VERSION_FILE = "game_versions/v1.0/version.txt"
GAME_EXECUTABLE = "game_versions/v1.0/game.py"  # path to your main game file

def read_version(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return "0.0"

def check_for_update():
    try:
        response = requests.get(UPDATE_URL, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except:
        return None  # if offline or failed

def run_updater():
    subprocess.run(["python", "update.py"])

def run_game():
    subprocess.run(["python", GAME_EXECUTABLE])

if __name__ == "__main__":
    local_version = read_version(LOCAL_VERSION_FILE)
    online_version = check_for_update()

    if online_version and online_version != local_version:
        run_updater()
    else:
        run_game()
