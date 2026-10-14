# Standardize VantaCrypt UI and project documentation.
import UI
from Functions.Action_Hist import push_hist
import random
import string

def password_generator(): 
    UI.header("Cryptographic Password Generator", "Customizable secure credential creation")
    push_hist("[*] Password generator was opened.")
    
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?"

    while True:
        try:
            len_str = UI.prompt_text("Enter desired password length (8 - 128)", default="16")
            password_length = int(len_str)
            if password_length < 8:
                UI.warning("Minimum secure length is 8 characters.")
                continue
            if password_length > 128:
                UI.warning("Maximum supported length is 128 characters.")
                continue
        except ValueError:
            UI.error("Please enter a valid number.")
            continue

        lower_needed = UI.prompt_confirm("Include lowercase characters (a-z)?", default=True)
        upper_needed = UI.prompt_confirm("Include uppercase characters (A-Z)?", default=True)
        digit_needed = UI.prompt_confirm("Include numerical digits (0-9)?", default=True)
        special_needed = UI.prompt_confirm("Include special symbols (!@#$)?", default=True)

        if not (lower_needed or upper_needed or digit_needed or special_needed):
            UI.warning("You must select at least one character type.")
            continue
        break

    password_chars = ""
    if lower_needed:
        password_chars += lowercase
    if upper_needed:
        password_chars += uppercase
    if digit_needed:
        password_chars += digits
    if special_needed:
        password_chars += special_characters

    password = "".join(random.choice(password_chars) for _ in range(password_length))
    UI.password_display(password)
    return password