import os
import json
import hashlib
import hmac
import binascii

PIN_FILE = "pin.json"
PBKDF2_ITERATIONS = 600000


def hash_new_pin(pin):
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, PBKDF2_ITERATIONS)
    return salt, hashed


def verify_pin(stored_salt, stored_hash, input_pin):
    new_hash = hashlib.pbkdf2_hmac("sha256", input_pin.encode(), stored_salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(new_hash, stored_hash)


def setup_pin(filepath=PIN_FILE):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            if "hash" in data:
                return
    except FileNotFoundError:
        pass

    pin = input("Create a PIN: ").strip()
    salt, hashed = hash_new_pin(pin)

    auth_data = {
        "salt": binascii.hexlify(salt).decode(),
        "hash": binascii.hexlify(hashed).decode(),
        "iterations": PBKDF2_ITERATIONS,
    }

    with open(filepath, "w") as f:
        json.dump(auth_data, f, indent=4)
    print("PIN created!")


def login(filepath=PIN_FILE):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return False

    for _ in range(3):
        pin = input("Enter PIN:").strip()
        if verify_pin(stored_salt, stored_hash, pin):
            print("Access granted.")
            return True
        print("Incorrect PIN.")

    print("Too many failed attempts. Exiting.")
    return False


def change_pin(filepath=PIN_FILE):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return

    current = input("Enter current PIN:").strip()
    if not verify_pin(stored_salt, stored_hash, current):
        print("Incorrect PIN.")
        return

    new_pin = input("Enter new PIN:").strip()
    new_salt, new_hash = hash_new_pin(new_pin)

    auth_data = {
        "salt": binascii.hexlify(new_salt).decode(),
        "hash": binascii.hexlify(new_hash).decode(),
        "iterations": PBKDF2_ITERATIONS,
    }

    with open(filepath, "w") as f:
        json.dump(auth_data, f, indent=4)
    print("PIN changed successfully.")
