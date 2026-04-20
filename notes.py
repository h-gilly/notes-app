from datetime import datetime

import json

import uuid

import os

import hashlib

import hmac

import binascii

print("Notes App Starting...")

PBKDF2_ITERATIONS = (
    600000  # high iteration count slows down brute force attacks. adjust if needed.
)


def hash_new_pin(pin):
    salt = os.urandom(
        16
    )  # generate a random salt so each hash is unique and resistant to rainbow table attacks
    hashed = hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), salt, PBKDF2_ITERATIONS
    )  # PBKDF2-HMAC-SHA256 with a high iteration count to make brute-force attempts expensive
    return salt, hashed


def verify_pin(stored_salt, stored_hash, input_pin):
    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        input_pin.encode(),
        stored_salt,
        PBKDF2_ITERATIONS,  # RE-derive the hash using stored salt and same PBKDF2 parameters
    )
    return hmac.compare_digest(
        new_hash, stored_hash
    )  # Constant-time comparison prevents timing attacks that leak information about the hash


def setup_pin():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            if "hash" in data:
                return
    except FileNotFoundError:
        pass

    pin = input("Create a PIN: ").strip()
    salt, hashed = hash_new_pin(
        pin
    )  # generate a secure salt + PBKDF2 hash of the new PIN. This way we never store the actual PIN, only a hash that is computationally expensive to reverse.

    auth_data = {  # store salt and hash in hex so they can be saved in JSON.
        "salt": binascii.hexlify(salt).decode(),
        "hash": binascii.hexlify(hashed).decode(),
        "iterations": PBKDF2_ITERATIONS,  # stored for future proofing or if we want to increase iterations later.
    }

    with open("pin.json", "w") as f:
        json.dump(auth_data, f, indent=4)

    print("PIN created!")


def login():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            # convert stored hex values back to bytes for verification.
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return False
    # allow 3 attempts to prevent unlimited brute-force guessing.
    for _ in range(3):
        pin = input("Enter PIN:").strip()
        if verify_pin(stored_salt, stored_hash, pin):
            print("Access granted.")
            return True
        print("Incorrect PIN.")

    print("Too many failed attempts. Exiting.")
    return False


def change_pin():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return
    # verify current PIN before allowing change to prevent unauthorized access if someone else has the file.
    current = input("Enter current PIN:").strip()
    if not verify_pin(stored_salt, stored_hash, current):
        print("Incorrect PIN.")
        return

    new_pin = input("Enter new PIN:").strip()
    new_salt, new_hash = hash_new_pin(
        new_pin
    )  # generate a fresh salt and hash for new PIN.

    auth_data = {
        "salt": binascii.hexlify(new_salt).decode(),
        "hash": binascii.hexlify(new_hash).decode(),
        "iterations": PBKDF2_ITERATIONS,
    }

    with open("pin.json", "w") as f:
        json.dump(auth_data, f, indent=4)
    print("PIN changed successfully.")


setup_pin()
if not login():
    exit()


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


def show_menu():
    print("1. Add a note")
    print("2. View notes")
    print("3. edit note")
    print("4. Search notes")
    print("5. Delete a note")
    print("6. Delete all notes")
    print("7. Change PIN")
    print("8. Exit")


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
        change_pin()

    elif choice == "8":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
