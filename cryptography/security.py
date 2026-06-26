import json
import os
import hashlib
import hmac
import binascii

print("Notes App Starting...")

PBKDF2_ITERATIONS = (
    600000  # high iteration count slows down brute force attacks. adjust if needed.
)


def hash_new_pin(pin):
    salt = os.urandom(
        16
    )  # generate a random salt so each hash is unique and resistant to rainbow table attacks
    hashed = hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), salt, PBKDF2_ITERATIONS
    )  # PBKDF2-HMAC-SHA256 with a high iteration count to make brute-force attempts expensive
    return salt, hashed


def verify_pin(stored_salt, stored_hash, input_pin):
    new_hash = hashlib.pbkdf2_hmac(
        "sha256",
        input_pin.encode(),
        stored_salt,
        PBKDF2_ITERATIONS,  # RE-derive the hash using stored salt and same PBKDF2 parameters
    )
    return hmac.compare_digest(
        new_hash, stored_hash
    )  # Constant-time comparison prevents timing attacks that leak information about the hash


def setup_pin():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            if "hash" in data:
                return
    except FileNotFoundError:
        pass

    pin = input("Create a PIN: ").strip()
    salt, hashed = hash_new_pin(
        pin
    )  # generate a secure salt + PBKDF2 hash of the new PIN. This way we never store the actual PIN, only a hash that is computationally expensive to reverse.

    auth_data = {  # store salt and hash in hex so they can be saved in JSON.
        "salt": binascii.hexlify(salt).decode(),
        "hash": binascii.hexlify(hashed).decode(),
        "iterations": PBKDF2_ITERATIONS,  # stored for future proofing or if we want to increase iterations later.
    }

    with open("pin.json", "w") as f:
        json.dump(auth_data, f, indent=4)

    print("PIN created!")


def login():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            # convert stored hex values back to bytes for verification.
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return False
    # allow 3 attempts to prevent unlimited brute-force guessing.
    for _ in range(3):
        pin = input("Enter PIN:").strip()
        if verify_pin(stored_salt, stored_hash, pin):
            print("Access granted.")
            return True
        print("Incorrect PIN.")

    print("Too many failed attempts. Exiting.")
    return False


def change_pin():
    try:
        with open("pin.json", "r") as f:
            data = json.load(f)
            stored_salt = binascii.unhexlify(data["salt"])
            stored_hash = binascii.unhexlify(data["hash"])
    except FileNotFoundError:
        print("PIN file missing.")
        return
    # verify current PIN before allowing change to prevent unauthorized access if someone else has the file.
    current = input("Enter current PIN:").strip()
    if not verify_pin(stored_salt, stored_hash, current):
        print("Incorrect PIN.")
        return

    new_pin = input("Enter new PIN:").strip()
    new_salt, new_hash = hash_new_pin(
        new_pin
    )  # generate a fresh salt and hash for new PIN.

    auth_data = {
        "salt": binascii.hexlify(new_salt).decode(),
        "hash": binascii.hexlify(new_hash).decode(),
        "iterations": PBKDF2_ITERATIONS,
    }

    with open("pin.json", "w") as f:
        json.dump(auth_data, f, indent=4)
    print("PIN changed successfully.")
