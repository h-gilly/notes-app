from datetime import datetime

import json

print("Notes App Starting...")

def load_notes():
    try:
        with open("notes.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [] # return empty list if file not found
    
def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=4) # save notes list to JSON with indentation


def add_note():
    # get note from user

    note_content = input("Write a note: ")

    # get current time stamp

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    notes = load_notes() # load existing notes from json

    new_entry = {"text": note_content, "timestamp": timestamp}

    notes.append(new_entry) # add new note to list
    save_notes(notes) # save updated notes list to json file

    print("Note added!")


def view_notes():
    try:
        notes = load_notes()

        # check if there are notes

        if not notes:
            print("No notes found.")
            return

        # display notes

        print("\n--- Your Notes ---")
        for i, note in enumerate(notes, start=1):
            print(f"{i}. {note['text']} ({note['timestamp']})")
        print("------------------\n")

    # handel notes file not found error

    except FileNotFoundError:
        print("no notes file yet.")


def edit_note():
    try:
        notes = load_notes()

            # stop if there are no notes

        if not notes:
                print("no notes to edit.")
                return

            # diplay notes with numbers

        print("\n--- Your Notes ---")
        for i, note in enumerate(notes, start=1):
                print(f"{i}. [{note['timestamp']}] {note['text']}")

            # ask user witch note to edit

        choice = input("\nEnter the number of the notes to edit: ")

            #  validate input

        if not choice.isdigit():
                print("Invalid choice.")
                return

        index = int(choice) - 1

            # check if number is in range

        if index < 0 or index >= len(notes):
                print("Note number out of range. ")
                return

            # get new text from user

        new_text = input("Enter the new text for the note: ").strip()

            # replace selected note

        notes[index]["text"] = new_text

        # save updated notes back to JSON

        save_notes(notes)

        print("Note updated successfuly.")

    except FileNotFoundError:
        print("No notes file found.")


def search_notes():
    # get search term from user

    term = input("Search for: ").strip()
    print("\nSearch results:")

    try:
        notes = load_notes()
        found = False

            # search for term in notes

        for n in notes:
            if term.lower() in n["text"].lower():
                 print(f"- {n['text']} ({n['timestamp']})")
                 found = True

            # if no matches found

            if not found:
                print("no matching notes found.")

        # handel file not found error

    except FileNotFoundError:
        print("No notes yet.")


def delete_note():
    print("\nDelete a note:")
    try:
        notes = load_notes()

            # check if there are notes

        if not notes:
                print("No notes to delete.")
                return

            # display notes with numbers
        print("\n--- Your Notes ---")
        for i, n in enumerate(notes, start=1):
                print(f"{i}. {n['text']} ({n['timestamp']})")
        
        num = input("Enter the number of the note to delete: ")

            # validate input

        if not num.isdigit() or int(num) < 1 or int(num) > len(notes):
                print("Invalid choice.")
                return

            # delete selected note

        index = int(num) - 1
        deleted_note = notes.pop(index)

            # save updated notes back to JSON

        save_notes(notes)
                
            # confirm deletion to user

        print(f"Deleted: {deleted_note['text']} ({deleted_note['timestamp']})")

        # handel file not found error

    except FileNotFoundError:
        print("No notes yet.")


def clear_all_notes():
    # confirm user wants to delete all notes

    confirm = input("Are you sure you want to delete ALL notes?  (y/n): ").lower()

    # if yes delete all notes

    if confirm == "y":
        save_notes([]) # overwrite JSON with empty list
        
        print("All notes have been cleared.")

    # if no cancel

    else:
        print("Canclled.")


def show_menu():
    # display menu options
    print("\nmenu:")
    print("1. Add a note")
    print("2. View notes")
    print("3. edit note")
    print("4. Search notes")
    print("5. Delete a note")
    print("6. Delete all notes")
    print("7. Exit")


while True:
    # show menu and get user choice

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
