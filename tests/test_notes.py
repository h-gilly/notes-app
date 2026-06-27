from src.notes import add_note_to_list, edit_note_in_list, delete_note_from_list, find_notes_by_term

def test_add_note_to_list():
    notes = []
    notes, note = add_note_to_list(notes, "Buy milk")
    assert len(notes) == 1
    assert note["text"] == "Buy milk"

def test_edit_note_in_list():
    notes = [{"text": "old", "last_modified": None}]
    notes, note = edit_note_in_list(notes, 0, "new")
    assert note["text"] == "new"
    assert note["last_modified"] is not None

def test_delete_note_from_list():
    notes = [{"text": "a"}, {"text": "b"}]
    notes, deleted = delete_note_from_list(notes, 0)
    assert deleted["text"] == "a"
    assert len(notes) == 1

def test_find_notes_by_term():
    notes = [{"text": "Buy milk"}, {"text": "Walk dog"}]
    results = find_notes_by_term(notes, "milk")
    assert len(results) == 1