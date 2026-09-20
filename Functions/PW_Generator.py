from Functions.Action_Hist import push_hist
import random
import string

def password_generator(): 
    push_hist('[*] Password generator was called.')
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"

    while True:
            password_length = int(input("Enter the desired password length (minimum 8): "))
            lower_needed = input("Do you want to include lowercase letters? (y/n): ").lower() == 'y'
            upper_needed = input("Do you want to include uppercase letters? (y/n): ").lower() == 'y'
            digit_needed = input("Do you want to include digits? (y/n): ").lower() == 'y'
            special_needed = input("Do you want to include special characters? (y/n): ").lower() == 'y'
            if password_length < 8:
                print("[!] Password length must be at least 8 characters.")
                continue
            if not (lower_needed or upper_needed or digit_needed or special_needed):
                print("[!] You must select at least one character type.")
                continue
            break
        
    password_chars = ''
    if lower_needed:
        password_chars += lowercase
    if upper_needed:
        password_chars += uppercase
    if digit_needed:
        password_chars += digits
    if special_needed:
        password_chars += special_characters

    password = ''.join(random.choice(password_chars) for _ in range(password_length))
    print(f"Generated Password: {password}")
