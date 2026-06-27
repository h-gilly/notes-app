from src.storage import load_notes, save_notes

from src.storage import load_notes, save_notes


def test_save_and_load_notes(tmp_path):
    file = tmp_path / "notes.json"
    notes = [{"text": "hello", "last_modified": None}]
    save_notes(notes, file)
    loaded = load_notes(file)
    assert loaded == notes