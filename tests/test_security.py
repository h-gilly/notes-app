from crypto_utils.security import hash_new_pin, verify_pin, setup_pin, login

def test_correct_pin_verifies():
    salt, hashed = hash_new_pin("1234")
    assert verify_pin(salt, hashed, "1234") is True

def test_wrong_pin_fails():
    salt, hashed = hash_new_pin("1234")
    assert verify_pin(salt, hashed, "0000") is False

def test_salts_are_random():
    salt1, _ = hash_new_pin("1234")
    salt2, _ = hash_new_pin("1234")
    assert salt1 != salt2

def test_setup_and_login(tmp_path, monkeypatch):
    file = tmp_path / "pin.json"
    monkeypatch.setattr("builtins.input", lambda _: "1234")  # simulates user typing "1234"
    setup_pin(file)
    assert file.exists()
    assert login(file) is True