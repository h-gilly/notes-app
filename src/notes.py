from datetime import datetime
from src.storage import load_notes, save_notes
from datetime import datetime
import uuid

# ---------- Pure logic functions ----------

def create_note(text):
    return {
        "id": str(uuid.uuid4()),
        "text": text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_modified": None,
    }


def add_note_to_list(notes, text):
    note = create_note(text)
    notes.append(note)
    return notes, note


def edit_note_in_list(notes, index, new_text):
    if index < 0 or index >= len(notes):
        return notes, None
    notes[index]["text"] = new_text
    notes[index]["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return notes, notes[index]


def delete_note_from_list(notes, index):
    if index < 0 or index >= len(notes):
        return notes, None
    note = notes.pop(index)
    return notes, note


def find_notes_by_term(notes, term):
    return [n for n in notes if term.lower() in n["text"].lower()]


# ---------- CLI wrappers ----------

def add_note():
    while True:
        text = input("Write a note: ")
        notes = load_notes()
        notes, _ = add_note_to_list(notes, text)
        save_notes(notes)
        print("Note added!")
        choice = input("Add another note? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            break


def view_notes():
    notes = load_notes()
    if not notes:
        print("No notes found.")
        return
    print("\n--- Your Notes ---")
    for i, n in enumerate(notes, start=1):
        print(f"{i}. [ID {n['id']}] {n['text']}")
        print(f"   Created: {n['timestamp']}")
        if n.get("last_modified"):
            print(f"   Last modified: {n['last_modified']}")


def edit_note():
    notes = load_notes()
    if not notes:
        print("no notes to edit.")
        return
    view_notes()
    choice = input("\nEnter the number of the note to edit: ").strip()
    if not choice.isdigit():
        print("Invalid choice.")
        return
    new_text = input("Enter the new text for the note: ").strip()
    notes, note = edit_note_in_list(notes, int(choice) - 1, new_text)
    if note is None:
        print("No note found with that number.")
        return
    save_notes(notes)
    print("Note updated successfully.")


def search_notes():
    term = input("Search for: ").strip()
    print("\n--- Search results ---")
    notes = load_notes()
    matches = find_notes_by_term(notes, term)
    if not matches:
        print("no matching notes found.")
        return
    for n in matches:
        print(f"- [ID {n['id']}] {n['text']} ({n['timestamp']})")
        if n.get("last_modified"):
            print(f"   Last modified: {n['last_modified']}")


def delete_note():
    notes = load_notes()
    if not notes:
        print("No notes to delete.")
        return
    view_notes()
    choice = input("\nEnter the number of the note to delete: ").strip()
    if not choice.isdigit():
        print("Invalid choice.")
        return
    notes, note = delete_note_from_list(notes, int(choice) - 1)
    if note is None:
        print("No note found with that number.")
        return
    save_notes(notes)
    print(f"Deleted: {note['text']}")


def clear_all_notes():
    confirm = input("Are you sure you want to delete ALL notes? (y/n): ").lower()
    if confirm == "y":
        save_notes([])
        print("All notes have been cleared.")
    else:
        print("Cancelled.")