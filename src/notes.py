from datetime import datetime
from src.storage import load_notes, save_notes
from datetime import datetime
import uuid

def add_note():
    # Loop allows adding multiple notes in one session without returning to the menu.
    while True:
        note_content = input("Write a note: ")
        notes = (
            load_notes()
        )  # Load existing notes so we append to the current list rather than overwriting.

        new_note = {
            "id": str(uuid.uuid4()),  # UUID ensures globally unique IDs for each note.
            "text": note_content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_modified": None,
        }

        notes.append(new_note)
        save_notes(notes)  # persist the updated list.

        print("Note added!")
        # Simple UX: pressing Enter or typing 'y' continues the loop to add another note, anything else returns to the menu.
        choice = input("Add another note? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            break


def view_notes():
    try:
        notes = load_notes()

        if not notes:
            print("No notes found.")
            return

        print("\n--- Your Notes ---")
        for i, n in enumerate(
            notes, start=1
        ):  # Enumerate so the user sees simple numbers instead of UUIDs.
            print(f"{i}. [ID {n['id']}] {n['text']}")
            print(f"   Created: {n['timestamp']}")
            if n.get("last_modified"):
                print(f"   Last modified: {n['last_modified']}")

    except FileNotFoundError:
        print("no notes file yet.")


def edit_note():
    try:
        notes = load_notes()

        if not notes:
            print("no notes to edit.")
            return

        print("\n--- Your Notes ---")
        for i, n in enumerate(
            notes, start=1
        ):  # Show numbered list so the user doesn't need to type UUIDs
            print(f"{i}. [ID {n['id']}] {n['text']}")
            print(f"  Created: {n['timestamp']}")
            if n.get("last_modified"):
                print(f"  Last modified: {n['last_modified']}")

        choice = input("\nEnter the number of the note to edit: ").strip()
        # Validate numeric input to avoid crashes.
        if not choice.isdigit():
            print("Invalid choice.")
            return

        index = int(choice) - 1
        if index < 0 or index >= len(
            notes
        ):  # Ensure the number corresponds to an actual note.
            print("No note found with that number.")
            return
        # Update note content and timestamp to track edits.
        note = notes[index]
        new_text = input("Enter the new text for the note: ").strip()

        note["text"] = new_text
        note["last_modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        save_notes(notes)

        print("Note updated successfuly.")

    except FileNotFoundError:
        print("No notes file found.")


def search_notes():
    term = input("Search for: ").strip()
    print("\n---  Search results ---")

    try:
        notes = load_notes()
        found = False
        # Case-insensitive search for a smoother UX. Shows all notes that contain the search term anywhere in the text.
        for n in notes:
            if term.lower() in n["text"].lower():
                print(f"- [ID {n['id']}] {n['text']} ({n['timestamp']})")
                if n.get(
                    "last_modified"
                ):  # Show last_modified only if the note was edited after creation.
                    print(f"   Last modified:  {n['last_modified']}")
                found = True

        if not found:
            print("no matching notes found.")

    except FileNotFoundError:
        print("No notes yet.")


def delete_note():
    print("\nDelete a note:")

    try:
        notes = load_notes()

        if not notes:
            print("No notes to delete.")
            return

        print("\n--- Your Notes ---")
        for i, n in enumerate(notes, start=1):
            print(f"{i}. [ID {n['id']}] {n['text']}")
            print(f"  Created: {n['timestamp']}")
            if n.get("last_modified"):
                print(f"  Last modified: {n['last_modified']}")

        choice = input("\nEnter the number of the note to delete: ").strip()

        if not choice.isdigit():
            print("Invalid choice.")
            return

        index = int(choice) - 1
        if index < 0 or index >= len(notes):
            print("No note found with that number.")
            return

        note = notes[index]
        # Remove the selected note and save the updated list
        notes.remove(note)
        save_notes(notes)

        print(f"Deleted: {note['text']}")
        print(f"Created: {note['timestamp']}")
        if note.get("last_modified"):
            print(f"Last modified: {note['last_modified']}")

    except FileNotFoundError:
        print("No notes yet.")


def clear_all_notes():
    confirm = input(
        "Are you sure you want to delete ALL notes?  (y/n): "
    ).lower()  # Confirmation prompt prevents accidental full data loss

    if confirm == "y":
        save_notes([])  # Overwrite notes.json with an empty list

        print("All notes have been cleared.")

    else:
        print("Canclled.")
