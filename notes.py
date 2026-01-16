from datetime import datetime 

print("Notes App Starting...")

def add_note():
    note = input("write a note: ")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open ("notes.txt", "a") as file: 
        file.write(f"[{timestamp}] {note}\n")

    print("Note saved!")

def view_notes():
    try:
        with open("notes.txt", "r") as file:
            notes = file.readlines()
        if not notes:
            print("No notes found.")
            return
        print("\n--- Your Notes ---")
        for i, note in enumerate(notes, start=1):
            print(f"{i}. {note.strip()}")
        print("------------------\n")

    except FileNotFoundError:
        print("no notes file yet.")
    
def search_notes():
    term = input("Search for: ")
    print("\nSearch results:")
            
    try:
        with open("notes.txt", "r") as file:
            notes = file.readlines()
            found = False
            for n in notes:
                if term.lower() in n.lower():
                    print("- " + n.strip())
                    found = True
            if not found:
                print("no matching notes found.")
    except FileNotFoundError:
        print("No notes yet.")

def delete_note():
    print("\nDelete a note:")
    try:
        with open("notes.txt", "r") as file:
            notes = file.readlines()
            if not notes:
                print("No notes to delete.")
                return
            for i, n in enumerate(notes, start=1):
                print(f"{i}. {n.strip()}")
            
            num = input("Enter the number of the note to delete: ")
                    
            if not num.isdigit() or int(num) < 1 or int(num) > len(notes):
                print("Invalid choice.")
                return

            index = int(num) - 1 
            deleted_note = notes.pop(index)
            
            with open("notes.txt", "w") as file:
                file.writelines(notes)

            print(f"Deleted: {deleted_note.strip()}")
    except FileNotFoundError:
        print("No notes yet.")
            
def clear_all_notes():
    confirm = input("Are you sure you want to delete ALL notes?  (y/n): ").lower()
    if confirm == "y":
        with open("notes.txt", "w") as file:
            file.write("") # overwrite with nothing

        print("All notes have been cleared.")
    else:
        print("Canclled.")

def show_menu():
    print("\nmenu:")
    print("1. Add a note")
    print("2. View notes")
    print("3. Search notes")
    print("4. Delete a note")
    print("5. Delete all notes")
    print("6. Exit")
     
while True:
    
    show_menu()
    choice = input("Choose and option: ")

    if choice == "1":
        add_note()
    
    elif choice == "2":
        view_notes()
                
    elif choice == "3":
       search_notes()
    
    elif choice == "4":
        delete_note()

    elif choice == "5":
        clear_all_notes()

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
        
    

      


