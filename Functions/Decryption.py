import os
import hashlib
import pickle
from rich.panel import Panel
from rich.text import Text
import UI

def min_decrypt(encrypted_file, encryption_key_file, uid):
    UI.header("Minimum Shift Decryption", "Reverse shift with UID watermarking")
    encrypted_file = str(encrypted_file) + ('' if str(encrypted_file).endswith('.txt') else '.txt')
    encryption_key_file = str(encryption_key_file) + ('' if str(encryption_key_file).endswith('.dat') else '.dat')

    if not os.path.exists(encrypted_file) or not os.path.exists(encryption_key_file):
        UI.error("Required encrypted file or key file is missing.")
        return

    try:
        with open(encrypted_file, 'r', encoding='utf-8') as f_txt:
            ciphertext_string = f_txt.read()

        with open(encryption_key_file, 'rb') as f_bin:
            security_payload = pickle.load(f_bin)

        keys = security_payload['keys']
        saved_uid = security_payload['uniqueid']

        if str(uid) != str(saved_uid):
            UI.error(f"ACCESS DENIED: File is watermarked to UID {saved_uid}. You do not have authorization.")
            return

        decrypted_chars = [chr(ord(char) - key) for char, key in zip(ciphertext_string, keys)]
        decrypted_text = "".join(decrypted_chars)

        UI.success("Decryption successful (Minimum Shift Mode)!")
        UI.console.print(Panel(
            Text(decrypted_text, style="bold white"),
            title="[bold success]DECRYPTED PAYLOAD[/bold success]",
            border_style="success",
            padding=(1, 2)
        ))
    except Exception as e:
        UI.error(f"Decryption error: {e}")

def inter_decrypt():
    UI.header("Intermediate Decryption", "Vigenère polyalphabetic cipher")
    UI.info("Intermediate Vigenère cipher is currently under active development.")

def max_decrypt(encrypted_file, encryption_key_file, current_uid):
    UI.header("Maximum XOR Stream Decryption", "Verify SHA-256 integrity and decrypt payload")
    encrypted_file = str(encrypted_file) + ('' if str(encrypted_file).endswith('.txt') else '.txt')
    encryption_key_file = str(encryption_key_file) + ('' if str(encryption_key_file).endswith('.dat') else '.dat')

    if not os.path.exists(encrypted_file) or not os.path.exists(encryption_key_file):
        UI.error("Required encrypted file or key file is missing.")
        return

    try:
        with open(encrypted_file, 'r', encoding='utf-8') as f_txt:
            hex_ciphertext = f_txt.read().strip()

        with open(encryption_key_file, 'rb') as f_bin:
            security_payload = pickle.load(f_bin)

        keys = security_payload['keys']
        saved_signature = security_payload['signature']
        saved_uid = security_payload['uniqueid']

        if str(current_uid) != str(saved_uid):
            UI.error(f"ACCESS DENIED: File is watermarked to UID {saved_uid}. You do not have authorization.")
            return

        encrypted_bytes = bytearray.fromhex(hex_ciphertext)
        decrypted_chars = [chr(byte ^ key) for byte, key in zip(encrypted_bytes, keys)]
        decrypted_text = "".join(decrypted_chars)

        decrypted_bytes = decrypted_text.encode('utf-8')
        new_hash = hashlib.sha256(decrypted_bytes).hexdigest()

        if new_hash == saved_signature:
            UI.success("INTEGRITY VERIFIED: SHA-256 hashes match. Data is authentic.")
            UI.console.print(Panel(
                Text(decrypted_text, style="bold white"),
                title="[bold success]AUTHENTIC DECRYPTED PAYLOAD[/bold success]",
                subtitle=f"SHA-256: {new_hash[:16]}...",
                border_style="success",
                padding=(1, 2)
            ))
        else:
            UI.error("CRITICAL INTEGRITY FAILURE: Hashes do not match. The file was tampered with!")
            UI.console.print(Panel(
                Text(decrypted_text, style="bold red"),
                title="[bold danger]CORRUPTED / TAMPERED PAYLOAD[/bold danger]",
                border_style="danger",
                padding=(1, 2)
            ))
    except Exception as e:
        UI.error(f"Decryption error: {e}")