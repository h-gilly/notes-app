from src.notes import (
    add_note,
    view_notes,
    edit_note,
    search_notes,
    delete_note,
    clear_all_notes
)

from cryptography.security  import change_pin

def show_menu():
    print("1. Add a note")
    print("2. View notes")
    print("3. edit note")
    print("4. Search notes")
    print("5. Delete a note")
    print("6. Delete all notes")
    print("7. Change PIN")
    print("8. Exit")

def run_menu():
    while True:
        show_menu()
        choice = input("Choose an option: ")

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
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")