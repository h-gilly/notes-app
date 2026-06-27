import json

NOTES_FILE = "notes.json"


def load_notes(filepath=NOTES_FILE):
    try:
        with open(filepath, "r") as file:
            notes = json.load(file)
        for n in notes:
            if "last_modified" not in n:
                n["last_modified"] = None
        return notes
    except FileNotFoundError:
        return []


def save_notes(notes, filepath=NOTES_FILE):
    with open(filepath, "w") as file:
        json.dump(notes, file, indent=4)
