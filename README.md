# Notes App (Python)
A simple command‑line notes application built using Python.
Supports adding, viewing, searching, editing, deleting and clearing notes. All stored in a structured JSON file with unique IDs

 ## Features
- 	Add notes with automatic timestamps
-  	Each note has unique incremental ID
-   View all saved notes in a clean, formatted list
- 	Search notes by keyword
-   Edit notes by selecting their ID
- 	Delete notes by selecting their ID
-   Clear all notes
-   Automatic `last_modified` timestamp when editing
- 	JSON storage

## How to Run

Tested with: **Python 3.12**

> **Windows note: when downloading `.py` files from the internet, Windows may show a security warning.
> This is a standard message for all Python scripts and not specific to this project.**

1. 	Clone the repository
2. 	No external dependencies required
3. 	Run the app: python notes.py

## Tech Used

- 	Python 3
- 	VS Code
- 	Standard library modules:
-   `datetime` for timestamps
- 	File I/O (`open`, `read`, `write`)

 ## Future Improvements

- 	More advanced formatting options
-   Add optional PIN lock for privacy
-   Store PIN securley using hashing (SHA-256)
-   Encrypt note text for full privacy in future version
-   Consider switching from incremental IDs to UUIDs
-   Add sorting options (newest first, alphabetical)
-   freeze and polish CLI version
- 	GUI version with CustomTkinter
