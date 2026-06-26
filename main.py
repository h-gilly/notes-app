from cryptography.security import setup_pin, login
from src.menu import show_menu
from src.notes import (
    add_note,
    view_notes,
    edit_note,
    search_notes,
    delete_note,
    clear_all_notes
)
from cryptography.security import change_pin

print("Notes App Starting...")

setup_pin()
if not login():
    exit()

while True:
    show_menu()
    choice = input("Choose an option: ").strip()

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
