import os
import secrets
import hashlib
import pickle
import random
import UI

def min_encrypt(encrypted_file, encryption_key_file, text, uid):
    UI.header("Minimum Shift Encryption", "Per-character dynamic shift cipher")
    if not text:
        UI.warning("Text to encrypt cannot be empty.")
        return

    encrypted_file = str(encrypted_file) + ('' if str(encrypted_file).endswith('.txt') else '.txt')
    encryption_key_file = str(encryption_key_file) + ('' if str(encryption_key_file).endswith('.dat') else '.dat')

    if os.path.exists(encrypted_file):
        UI.warning(f"File '{encrypted_file}' already exists and will be overwritten.")
    if os.path.exists(encryption_key_file):
        UI.warning(f"Key file '{encryption_key_file}' already exists and will be overwritten.")

    keys = []
    encrypted_chars = []
    for char in text:
        shift = random.randint(-20, 20)
        keys.append(shift)
        encrypted_chars.append(chr(ord(char) + shift))

    encrypted_text = "".join(encrypted_chars)

    try:
        with open(encrypted_file, "w", encoding="utf-8") as f_txt:
            f_txt.write(encrypted_text)

        with open(encryption_key_file, "wb") as f_bin:
            pickle.dump({"keys": keys, "uniqueid": uid}, f_bin)

        UI.success("Data successfully encrypted!")
        UI.cipher_summary("Encryption", "Minimum Dynamic Shift", encrypted_file, encryption_key_file)
    except Exception as e:
        UI.error(f"Failed to write encrypted files: {e}")

def inter_encrypt():
    UI.header("Intermediate Encryption", "Vigenère polyalphabetic cipher")
    UI.info("Intermediate Vigenère cipher is currently under active development.")

def max_encrypt(text, encrypted_file, encryption_key_file, UID):
    UI.header("Maximum XOR Stream Encryption", "Cryptographic stream cipher with SHA-256 signature")
    if not text:
        UI.warning("Text to encrypt cannot be empty.")
        return

    encrypted_file = str(encrypted_file) + ('' if str(encrypted_file).endswith('.txt') else '.txt')
    encryption_key_file = str(encryption_key_file) + ('' if str(encryption_key_file).endswith('.dat') else '.dat')

    if os.path.exists(encrypted_file):
        UI.warning(f"File '{encrypted_file}' already exists and will be overwritten.")
    if os.path.exists(encryption_key_file):
        UI.warning(f"Key file '{encryption_key_file}' already exists and will be overwritten.")

    text_bytes = text.encode("utf-8")
    og_hash = hashlib.sha256(text_bytes).hexdigest()

    keys = [secrets.randbelow(256) for _ in text]
    encrypted_integers = [ord(char) ^ key for char, key in zip(text, keys)]
    hex_ciphertext = bytearray(encrypted_integers).hex()

    security_payload = {
        "keys": keys,
        "signature": og_hash,
        "uniqueid": UID
    }

    try:
        with open(encrypted_file, "w", encoding="utf-8") as f_txt:
            f_txt.write(hex_ciphertext)

        with open(encryption_key_file, "wb") as f_bin:
            pickle.dump(security_payload, f_bin)

        UI.success("Cryptographic grade encryption complete!")
        UI.cipher_summary("Encryption", "Maximum XOR Stream + SHA-256", encrypted_file, encryption_key_file, og_hash)
    except Exception as e:
        UI.error(f"Encryption failed: {e}")