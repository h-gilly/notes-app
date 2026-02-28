from datetime import datetime

import json

print("Notes App Starting...")


def load_notes():
    try:
        with open("notes.json", "r") as file:
            return json.load(file)

        for n in notes:
            if "last_modified" not in n:
                n["last_modified"] = None
            if "id" not in n:
                n["id"] = None

        next_id = 1
        for n in notes:
            if n.get("id") is None:
                n["id"] = next_id
                next_id += 1
            else:
                next_id = max(next_id, n["id"] + 1)

        return notes

    except FileNotFoundError:
        return []


def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4)


def generate_id(notes):
    if not notes:
        return 1
    return max(n["id"] for n in notes) + 1


def add_note():

    note_content = input("Write a note: ")

    notes = load_notes()

    new_note = {
        "id": generate_id(notes),
        "text": note_content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_modified": None,
    }

    notes.append(new_note)
    save_notes(notes)

    print("Note added!")


def view_notes():
    try:
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

    except FileNotFoundError:
        print("no notes file yet.")


def edit_note():
    try:
        notes = load_notes()

        if not notes:
            print("no notes to edit.")
            return

        print("\n--- Your Notes ---")
        for i, n in enumerate(notes, start=1):
            print(f"{i}. [ID {n['id']}] {n['text']}")
            print(f"  Created: {n['timestamp']}")
            if n.get("last_modified"):
                print(f"  Last modified: {n['last_modified']}")

        choice = input("\nEnter the ID of the note to edit: ")

        if not choice.isdigit():
            print("Invalid ID.")
            return

        note_id = int(choice)

        note = next((n for n in notes if n["id"] == note_id), None)

        if not note:
            print("No note found with that ID.")
            return

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

        for n in notes:
            if term.lower() in n["text"].lower():
                print(f"- [ID {n['id']}] {n['text']} ({n['timestamp']})")
                if n.get("last_modified"):
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

        num = input("\nEnter the ID of the note to delete: ")

        if not num.isdigit():
            print("Invalid ID.")
            return

        note_id = int(num)

        note = next((n for n in notes if n["id"] == note_id), None)

        if not note:
            print("No note found with that ID.")
            return

        notes.remove(note)
        save_notes(notes)

        print(f"Deleted: {note['text']}")
        print(f"Created: {note['timestamp']}")
        if note.get("last_modified"):
            print(f"Last modified: {note['last_modified']}")

    except FileNotFoundError:
        print("No notes yet.")


def clear_all_notes():
    confirm = input("Are you sure you want to delete ALL notes?  (y/n): ").lower()

    if confirm == "y":
        save_notes([])

        print("All notes have been cleared.")

    else:
        print("Canclled.")


def show_menu():
    print("1. Add a note")
    print("2. View notes")
    print("3. edit note")
    print("4. Search notes")
    print("5. Delete a note")
    print("6. Delete all notes")
    print("7. Exit")


while True:

    show_menu()
    choice = input("Choose and option: ")

    if choice == "1":
        add_note()

    elif choice == "2":
        view_notes()

    elif choice == "3":
        edit_note()

    elif choice == "4":
        search_notes()

    elif choice == "5":
        delete_note()

    elif choice == "6":
        clear_all_notes()

    elif choice == "7":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
