# Notes App (Python)

![CI](https://github.com/h-gilly/notes-app/actions/workflows/test.yml/badge.svg)

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

The project is organised into clear modules to support testability, separation of concerns, and maintainability:

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
├── crypto_utils/
│   ├── __init__.py
│   └── security.py
│
├── tests/
    ├──test_security.py
    ├──test_notes.py
    └──test_storage.py
```

## How It Works (Architecture)

The project is intentionally structured to separate concerns:

### 1. Pure Logic (testable)

`notes.py` contains pure functions such as:

- `add_note_to_list`
- `edit_note_in_list`
- `delete_note_from_list`
- `find_notes_by_term`

These functions take data as input and return new data without printing or reading input.
This makes them fully unit-testable.

### 2. CLI Wrappers

Functions like `add_note()` and `edit_note()` handle:

- user input
- printing
- calling the pure logic functions
- saving data

### 3. Storage Layer

`storage.py` provides:

- `load_notes(path=...)`
- `save_notes(path=...)`

The optional `path` parameter allows tests to inject temporary files.

### 4. Security Layer

`crypto_utils/security.py` handles:

- PIN hashing (PBKDF2)
- PIN verification
- PIN changes

No security code runs on import; all logic is triggered from `main.py`.

### 5. Entry Point

`main.py` orchestrates:

- PIN setup
- login
- menu loop

## How to Run

Tested with: **Python 3.12**

On first run, you will be prompted to create a PIN.
On later runs, you must enter the PIN to access your notes.

1. Clone the repository
2. No external dependencies required
3. Run the app:

```code
python main.py
```

## Requirements

- Python 3.12+
- pytest (for running tests)

## Development Setup

Create a virtual environment (recommended):

python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

Install test dependencies (for local testing):

```code
pip install pytest
```

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

### Why This Architechture?

This structure follows best practices for junior backend development:

- Pure logic functions for testability
- Thin CLI wrappers for user interaction
- A dedicated storage layer with dependency injection
- A security module isolated from business logic
- A single entry point (main.py) that orchestrates the app

## Tests

This project includes a full pytest suite covering:

- **Notes logic** (pure functions for add/edit/delete/search)
- **Storage layer** (load/save using dependency-injected file paths)
- **Security utilities** (PIN hashing and verification)

All tests are isolated, deterministic, and do not touch real user data.
Temporary files are created using pytest's `tmp_path` fixture.

Run the full test suite:

```code
pytest -v
```

Example output: 9 passed in 1.72s

## Future Improvements

- More advanced formatting options
- Encrypt notes instead of plain JSON
- Add sorting options (newest first, alphabetical)
- Add a backup\restore system
- Export notes to a `.txt` file
- Add caching for faster repeated operations
- Add cloud sync
- Add a REST API version
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
