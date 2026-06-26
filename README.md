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
- Timing-safe comparison using hmac.compare_digest()
- Random 16‑byte salt + 600,000 iterations

### Notes Management

- Add notes with automatic timestamps
- Add multiple notes in one session without returning to the menu
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

### File structure

```code
project/
│
├── main.py
│
├── src/
│   ├── __init__.py
│   ├── menu.py
│   ├── notes.py
│   └── storage.py
│
└── cryptography/
    ├── __init__.py
    └── security.py

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

## Why These Technical Choices?

### PBKDF2‑HMAC‑SHA256

Used for secure PIN hashing. PBKDF2 is intentionally slow, making brute‑force attacks expensive. Combined with HMAC‑SHA256, it provides strong, modern protection suitable for real authentication systems.

### Random Salt (16 bytes)

Prevents rainbow‑table attacks and ensures each user’s hash is unique, even if they choose the same PIN.

### hmac.compare_digest()

Prevents timing attacks by ensuring comparisons take constant time regardless of input.

### UUID4

Generates random, collision‑resistant IDs without needing a database or incremental counters. Ideal for syncing, merging, or future multi‑device support.

### CRUD Structure

Implements the core operations used in almost all backend systems. Building CRUD manually teaches real data‑flow, state management, and backend logic.

### JSON Storage

Lightweight, human‑readable, and perfect for a CLI tool. Allows structured storage without requiring a database. Easy to debug and portable.

## Future Improvements

- More advanced formatting options
- Encrypt notes instead of plain JSON
- Add sorting options (newest first, alphabetical)
- Add a backup\restore system
- Export notes to a `.txt` file
- Add caching for faster repeated operations
- Freeze and polish the CLI version
- GUI version with CustomTkinter

### OpenAI API Integration

- Planned features using OpenAI models:

- Automatic note summaries

- Grammar/spell correction

- Topic tagging

- Quick “rewrite” or “expand” actions

- This will turn the notes app into a smart assistant instead of just a storage tool.

### C# Notes Viewer (Rewrite Project)

A GUI‑based viewer written in C#/.NET to complement the Python backend.
Focus areas:

- Clean architecture

- Data handling

- Cross‑platform UI
