# Notes App (Python)

A simple command‑line notes application built using Python.
Supports adding, viewing, searching, editing, deleting, and clearing notes.
All notes are stored in a structured JSON file with UUID‑based unique IDs.
Now includes a secure PIN lock using PBKDF2‑HMAC‑SHA256 with a random salt and 600k iterations.

## Features

### Security

- PIN‑protected access
- First run: create a PIN
- Future runs: enter PIN to unlock
- 3 attempts before exit
- Change PIN at any time
- PIN stored securely using  PBKDF2‑HMAC‑SHA256
- Random 16‑byte salt + 600,000 iterations

### Notes Management

- Add notes with automatic timestamps
- Each note has a  UUID4 unique ID
- Edit and delete notes using simple number‑based selection
- View all notes in a clean formatted list
- Search notes by keyword
- Clear all notes

### Metadata & Storage

- Automatic `last_modified`  timestamp when editing
- Notes stored in `notes.json`
- PIN stored in `pin.json`
- No external dependencies required

### file structure

```
project/
│
├── notes.json      # Created automatically when notes are saved
├── pin.json        # Created automatically on first run (stores hashed PIN)
└── notes.py        # Main application
```

## How to Run

Tested with: **Python 3.12**

On first run, you will be prompted to create a PIN.
On later runs, you must enter the PIN to access your notes.

> **Windows note:** when downloading `.py` files from the internet, Windows may show a security warning.
> This is a standard message for all Python scripts and not specific to this project.**

1. Clone the repository
2. No external dependencies required
3. Run the app: python notes.py

## Tech Used

- Python 3
- VS Code
- Standard library modules:
- `datetime` for timestamps
  `json` for storage
  `hashlib` for secure PIN hashing
- File I/O (`open`, `read`, `write`)

## Future Improvements

- More advanced formatting options
- Encrypt notes instead of plan JSON
- Add sorting options (newest first, alphabetical)
- Add a backup\restore system
- Export notes to a `.txt` file
- Add caching for faster repeated operations
- freeze and polish CLI version
- GUI version with CustomTkinter
