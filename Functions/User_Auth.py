import os
import csv
import random
import UI

USER_DATA_DIR = os.path.join("Data", "UserData")
USER_DATA_FILE = os.path.join(USER_DATA_DIR, "user_data.csv")

def _ensure_user_file():
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Username", "Password", "UniqueID"])

def login():
    _ensure_user_file()
    UI.header("User Authentication Portal", "Sign in with your master credentials")
    username = UI.prompt_text("Enter username")
    if not username:
        UI.warning("Username cannot be empty. Aborted.")
        return None, None

    password = UI.prompt_secret("Enter password")
    if not password:
        UI.warning("Password cannot be empty. Aborted.")
        return None, None

    try:
        with open(USER_DATA_FILE, "r", newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                if row and len(row) >= 3 and row[0].lower() != "username":
                    if row[0] == username and row[1] == password:
                        UI.success(f"Access granted: Welcome back, {username}!")
                        UI.set_user(username, row[2])
                        return row[2], row[1]
    except Exception as e:
        UI.error(f"Error accessing user database: {e}")
        return None, None

    UI.error("Invalid credentials: Username or password does not match.")
    return None, None

def register():
    _ensure_user_file()
    UI.header("New User Registration", "Enroll in the VantaCrypt security system")
    username = UI.prompt_text("Choose a username")
    if not username:
        UI.warning("Username cannot be empty. Aborted.")
        return False
    elif username.lower() == "username":
        UI.error("'username' is a reserved identifier and cannot be registered.")
        return False

    existing_users = []
    existing_ids = []
    with open(USER_DATA_FILE, "r", newline="", encoding="utf-8") as g:
        for row in csv.reader(g):
            if row and len(row) >= 3 and row[0].lower() != "username":
                existing_users.append(row[0].lower())
                existing_ids.append(str(row[2]))

    if username.lower() in existing_users:
        UI.error("User already exists! Please log in instead.")
        return False

    password = UI.prompt_secret("Create a master password")
    if not password:
        UI.warning("Password cannot be empty. Aborted.")
        return False

    re_password = UI.prompt_secret("Confirm master password")
    if password != re_password:
        UI.error("Password confirmation mismatch. Registration aborted.")
        return False

    while True:
        unique_id = str(random.randint(10000000, 99999999))
        if unique_id not in existing_ids:
            break

    try:
        with open(USER_DATA_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([username, password, unique_id])
        UI.success(f"Account successfully registered! Assigned UID: {unique_id}")
        return True
    except Exception as e:
        UI.error(f"Failed to record registration: {e}")
        return False