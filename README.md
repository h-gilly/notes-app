# Notes App (Python)
A simple command‑line notes application built using Python.
Supports adding, viewing, searching, editing, deleting and clearing notes. All stored in a structured JSON file.

 ## Features
- 	Add notes with automatic timestamps
-  	View all saved notes in a numbered list
- 	Search notes by keyword
-   Edit existing notes
- 	Delete notes by selecting their number
-   Clear all notes
-   Improved formatting when viewing notes
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
-   Add optinal PIN lock for privacy
-   Store PIN securley using hashing
-   Encrypt notes in the future for full privacy
-   freeze CLI version
- 	GUI version with CustomTkinter
