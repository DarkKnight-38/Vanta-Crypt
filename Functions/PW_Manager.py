import os
import pickle
import UI
from Functions.Action_Hist import push_hist
from Functions.PW_Generator import password_generator

VAULT_DIR = os.path.join("Data", "PWManagerData")

def _get_vault_file(UID):
    os.makedirs(VAULT_DIR, exist_ok=True)
    return os.path.join(VAULT_DIR, f"password_vault_{UID}.dat")

def _load_vault(UID):
    file_name = _get_vault_file(UID)
    data = []
    if os.path.exists(file_name):
        try:
            with open(file_name, "rb") as f:
                while True:
                    try:
                        entry = pickle.load(f)
                        if isinstance(entry, dict):
                            data.append(entry)
                    except EOFError:
                        break
        except Exception as e:
            UI.warning(f"Note: Error reading vault records ({e}).")
    return data

def _save_vault(UID, data):
    file_name = _get_vault_file(UID)
    try:
        with open(file_name, "wb") as f:
            for entry in data:
                pickle.dump(entry, f)
        return True
    except Exception as e:
        UI.error(f"Failed to write vault data: {e}")
        return False

def add(UID):
    UI.header("Password Vault / Add Credential", "Store website access details securely")
    push_hist("[*] Password manager add() was called.")
    data = _load_vault(UID)

    website = UI.prompt_text("Website or Service name")
    if not website:
        UI.warning("Website name cannot be empty. Aborted.")
        return

    for entry in data:
        if entry.get("Website", "").lower() == website.lower():
            UI.error("An entry for this website already exists in your vault.")
            return

    username = UI.prompt_text("Username or Email")
    if not username:
        UI.warning("Username cannot be empty. Aborted.")
        return

    use_gen = UI.prompt_confirm("Generate a cryptographically secure password?", default=True)
    if use_gen:
        password = password_generator()
    else:
        password = UI.prompt_secret("Enter account password")
        if not password:
            UI.warning("Password cannot be empty. Aborted.")
            return

    notes = UI.prompt_text("Additional notes (optional)")

    new_entry = {
        "Website": website,
        "Username": username,
        "Password": password,
        "Notes": notes,
        "UID": UID
    }
    data.append(new_entry)
    if _save_vault(UID, data):
        UI.success(f"Credential for '{website}' successfully encrypted and saved to vault!")
        push_hist(f"[*] Added new vault credential for {website}.")

def view(UID, password):
    UI.header("Password Vault / View Credentials", "Authenticate to unlock credential table")
    push_hist("[*] Password manager view() was called.")
    data = _load_vault(UID)

    if not data:
        UI.info("Your vault is empty. Use 'Add' to store your first credential.")
        return

    entered_pw = UI.prompt_secret("Enter master account password to unlock")
    if entered_pw != password:
        UI.error("Access Denied: Incorrect master password.")
        push_hist("[!] Unauthorized attempt to view password vault.")
        return

    UI.success("Master password verified. Vault unlocked.")
    UI.vault_table(data)

def remove(UID, password):
    UI.header("Password Vault / Remove Credential", "Delete account record permanently")
    push_hist("[*] Password manager remove() was called.")
    data = _load_vault(UID)

    if not data:
        UI.info("Your vault is currently empty.")
        return

    entered_pw = UI.prompt_secret("Enter master account password to authorize deletion")
    if entered_pw != password:
        UI.error("Access Denied: Incorrect master password.")
        push_hist("[!] Unauthorized attempt to remove credential.")
        return

    website = UI.prompt_text("Enter website/service name to remove")
    target = None
    for entry in data:
        if entry.get("Website", "").lower() == website.lower():
            target = entry
            break

    if not target:
        UI.error(f"No entry found matching '{website}'.")
        return

    confirm = UI.prompt_confirm(f"Are you sure you want to permanently delete credentials for '{target['Website']}'?", default=False)
    if confirm:
        data.remove(target)
        if _save_vault(UID, data):
            UI.success(f"Credential for '{website}' removed from vault.")
            push_hist(f"[*] Removed vault credential for {website}.")
    else:
        UI.info("Deletion cancelled.")

def edit(UID, password):
    UI.header("Password Vault / Edit Credential", "Update existing credentials")
    push_hist("[*] Password manager edit() was called.")
    data = _load_vault(UID)

    if not data:
        UI.info("Your vault is currently empty.")
        return

    entered_pw = UI.prompt_secret("Enter master account password to authorize edit")
    if entered_pw != password:
        UI.error("Access Denied: Incorrect master password.")
        return

    website = UI.prompt_text("Enter website name of the entry to modify")
    target = None
    for entry in data:
        if entry.get("Website", "").lower() == website.lower():
            target = entry
            break

    if not target:
        UI.error(f"No entry found matching '{website}'.")
        return

    UI.info(f"Editing entry: {target['Website']}")
    new_user = UI.prompt_text(f"New Username (current: {target['Username']})", default=target['Username'])
    
    change_pw = UI.prompt_confirm("Do you want to update the password?", default=False)
    if change_pw:
        use_gen = UI.prompt_confirm("Generate a new random password?", default=True)
        if use_gen:
            new_pw = password_generator()
        else:
            new_pw = UI.prompt_secret("Enter new password")
        if new_pw:
            target["Password"] = new_pw

    new_notes = UI.prompt_text(f"New Notes (current: {target.get('Notes', '')})", default=target.get('Notes', ''))
    target["Username"] = new_user
    target["Notes"] = new_notes

    if _save_vault(UID, data):
        UI.success(f"Updated credentials for '{target['Website']}'.")
        push_hist(f"[*] Edited vault entry for {target['Website']}.")