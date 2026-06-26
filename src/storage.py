
import json

def load_notes():
    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
        # Older notes may not have a last_modified field → ensure consistent structure
        for n in notes:
            if "last_modified" not in n:
                n["last_modified"] = None

        return notes

    except FileNotFoundError:
        return []


def save_notes(notes):
    # Save notes with indentation for readability and version control clarity.
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4)
