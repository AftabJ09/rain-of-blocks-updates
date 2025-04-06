import tkinter as tk
from tkinter import messagebox
import requests, zipfile, io, os, shutil
import subprocess

ZIP_URL = "https://github.com/AftabJ09/rain-of-blocks-updates/raw/main/Rain-of-Blocks-v1.1.zip"
DEST_FOLDER = "game_versions/v1.0"
VERSION_FILE = "game_versions/v1.0/version.txt"
UPDATE_URL = "https://raw.githubusercontent.com/AftabJ09/rain-of-blocks-updates/main/version.txt"
response = requests.get(UPDATE_URL)
NEW_VERSION = response.text.strip()  


def download_and_replace():
    response = requests.get(ZIP_URL)
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        # Clean old version
        if os.path.exists(DEST_FOLDER):
            shutil.rmtree(DEST_FOLDER)
        zip_ref.extractall(DEST_FOLDER)

    # Write new version
    with open(VERSION_FILE, 'w') as f:
        f.write(NEW_VERSION)

    # Show success and launch game
    messagebox.showinfo("Update Complete", "Game updated to v" + NEW_VERSION)
    subprocess.Popen(["python", os.path.join(DEST_FOLDER, "game.py")])
    root.destroy()

root = tk.Tk()
root.withdraw()  # Hide main window

answer = messagebox.askyesno("Update Available", "A new version is available. Please Update")
if answer:
    download_and_replace()
else:
    root.destroy()
