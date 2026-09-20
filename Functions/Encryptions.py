import secrets
import os
import hashlib
import pickle
import random
def min_encrypt(encrypted_file, encryption_key_file, text, uid):
    encrypted_file=str(encrypted_file)+'.txt'
    encryption_key_file=str(encryption_key_file)+'.dat'
    keys=[]
    encrypted_text=""
    text_length=len(text)
    if os.path.exists(encrypted_file):
        print(f"[!] WARNING: The file '{encrypted_file}' already exists and will be overwritten.")
    if os.path.exists(encryption_key_file):
        print(f"[!] WARNING: The file '{encryption_key_file}' already exists and will be overwritten.")
    if encrypted_file=='' or encryption_key_file=='':
        print(f"[!] WARNING: File name cannot be empty")
        return
    for i in range(text_length):
        random_shift=random.randint(-20,20)
        keys.append(random_shift)

        char_code=ord(text[i])
        shifted_code=char_code+random_shift
        encrypted_text+=chr(shifted_code)

    with open (encrypted_file,'w', encoding='utf-8') as f_txt:
        f_txt.write(encrypted_text)

    with open (encryption_key_file,'wb') as f_bin:
        payload={'keys':keys,'uniqueid':uid}
        pickle.dump(payload,f_bin)

    print()
    print("[*] SUCCESS: Data Encrypted.")
    output_msg_part_1 = " > Ciphertext written to : "
    final_output_1 = output_msg_part_1 + str(encrypted_file)
    print(final_output_1)
    
    output_msg_part_2 = " > Keys & UID written to : "
    final_output_2 = output_msg_part_2 + str(encryption_key_file)
    print(final_output_2) 
    print()

def inter_encrypt():
    pass
def max_encrypt(text, encrypted_file, encryption_key_file, UID):
    encrypted_file=str(encrypted_file)+'.txt'
    encryption_key_file=str(encryption_key_file)+'.dat'
    
    encoding_format = 'utf-8'
    text_bytes = text.encode(encoding_format)
    
    hash_generator = hashlib.sha256()
    hash_generator.update(text_bytes)
    og_hash = hash_generator.hexdigest()
    
    keys = []
    text_length = len(text)

    if os.path.exists(encrypted_file):
        print(f"[!] WARNING: The file '{encrypted_file}' already exists and will be overwritten.")
    if os.path.exists(encryption_key_file):
        print(f"[!] WARNGING: The file '{encryption_key_file}' already exists and will be overwritten.")
    if encrypted_file=='' or encryption_key_file=='':
        print(f"[!] WARNING: File name cannot be empty")
        return
    for i in range(text_length):
        random_value = secrets.randbelow(256)
        keys.append(random_value)
        
    encrypted_integers = []
    index_tracker = 0
    
    for char in text:
        char_code = ord(char)
        current_key = keys[index_tracker]
        xored_value = char_code ^ current_key
        encrypted_integers.append(xored_value)
        index_tracker += 1
        
    encrypted_bytes_array = bytearray(encrypted_integers)
    hex_formatted_ciphertext = encrypted_bytes_array.hex()
    
    text_file_object = open(encrypted_file, 'w')
    text_file_object.write(hex_formatted_ciphertext)
    text_file_object.close()
    
    security_payload = dict()
    
    security_payload['keys'] = keys
    security_payload['signature'] = og_hash
    security_payload['uniqueid'] = UID
    
    binary_file_object = open(encryption_key_file, 'wb')
    pickle.dump(security_payload, binary_file_object)
    binary_file_object.close()
    
    print()
    print("[*] SUCCESS: Data Encrypted.")
    
    output_msg_part_1 = " > Ciphertext written to : "
    final_output_1 = output_msg_part_1 + str(encrypted_file)
    print(final_output_1)
    
    output_msg_part_2 = " > Keys & Hash written to: "
    final_output_2 = output_msg_part_2 + str(encryption_key_file)
    print(final_output_2)
    print()