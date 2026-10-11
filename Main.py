import sys
import os

import UI
import Functions.Action_Hist as Action_Hist
import Functions.Encryptions as Encryptions
import Functions.Decryption as Decryption
import Functions.Graph as Graph
import Functions.PW_Generator as PW_Generator
import Functions.PW_Strength as PW_Strength
import Functions.User_Auth as User_Auth
import Functions.PW_Manager as PW_Manager


def encryption_menu(UID):
    while True:
        UI.clear_screen()
        UI.show_banner()
        UI.status_header(actions_count=len(Action_Hist.history))
        
        choice = UI.menu(
            "Encryption & Decryption Suite",
            [
                ("1", "🔒 Maximum (XOR Stream + SHA-256)", "Cryptographic stream cipher with SHA-256 integrity"),
                ("2", "🔤 Minimum (Dynamic Shift)", "Per-character dynamic shift cipher with UID lock"),
                ("3", "⚙️ Intermediate (Vigenère)", "Polyalphabetic substitution cipher (in development)"),
                ("B", "↩  Back to Main Menu", "Return to main command center")
            ],
            default="1"
        )

        if choice == "1":
            UI.header("Maximum Encryption / Decryption")
            action = UI.menu(
                "Choose Maximum Cipher Operation",
                [
                    ("E", "🔒 Encrypt Text to File", "Generate ciphertext and hashed security payload"),
                    ("D", "🔓 Decrypt File", "Verify SHA-256 integrity and restore original text"),
                    ("B", "↩  Cancel", "Return to cipher options")
                ],
                default="E"
            )
            if action == "E":
                text = UI.prompt_text("Enter text to encrypt")
                if text:
                    txt_file = UI.prompt_filepath("Output ciphertext filename (without extension)")
                    enc_key = UI.prompt_filepath("Output key filename (without extension)")
                    Encryptions.max_encrypt(text, txt_file, enc_key, UID)
            elif action == "D":
                txt_file = UI.prompt_filepath("Ciphertext filename to decrypt")
                enc_key = UI.prompt_filepath("Key filename")
                Decryption.max_decrypt(txt_file, enc_key, UID)
            UI.prompt_text("Press Enter to continue...")

        elif choice == "2":
            UI.header("Minimum Encryption / Decryption")
            action = UI.menu(
                "Choose Minimum Cipher Operation",
                [
                    ("E", "🔒 Encrypt Text to File", "Apply random per-character shift"),
                    ("D", "🔓 Decrypt File", "Reverse shift with UID check"),
                    ("B", "↩  Cancel", "Return to cipher options")
                ],
                default="E"
            )
            if action == "E":
                text = UI.prompt_text("Enter text to encrypt")
                if text:
                    txt_file = UI.prompt_filepath("Output .txt filename")
                    enc_key = UI.prompt_filepath("Output key .dat filename")
                    Encryptions.min_encrypt(txt_file, enc_key, text, UID)
            elif action == "D":
                txt_file = UI.prompt_filepath("Ciphertext .txt filename to decrypt")
                enc_key = UI.prompt_filepath("Key .dat filename")
                Decryption.min_decrypt(txt_file, enc_key, UID)
            UI.prompt_text("Press Enter to continue...")

        elif choice == "3":
            Encryptions.inter_encrypt()
            UI.prompt_text("Press Enter to continue...")

        elif choice.upper() == "B":
            break


def vault_menu(UID, password):
    while True:
        UI.clear_screen()
        UI.show_banner()
        vault_count = len(PW_Manager._load_vault(UID)) if hasattr(PW_Manager, '_load_vault') else None
        UI.status_header(actions_count=len(Action_Hist.history), vault_count=vault_count)
        
        choice = UI.menu(
            "Password Manager & Credential Vault",
            [
                ("1", "👁️  View Saved Credentials", "Authenticate to unlock and view credential table"),
                ("2", "➕ Add New Credential", "Store a new website login, password, and notes"),
                ("3", "✏️  Edit Credential", "Update an existing account's details"),
                ("4", "🗑️  Remove Credential", "Delete a credential record from the vault"),
                ("B", "↩  Back to Main Menu", "Return to main command center")
            ],
            default="1"
        )

        if choice == "1":
            PW_Manager.view(UID, password)
            UI.prompt_text("Press Enter to continue...")
        elif choice == "2":
            PW_Manager.add(UID)
            UI.prompt_text("Press Enter to continue...")
        elif choice == "3":
            PW_Manager.edit(UID, password)
            UI.prompt_text("Press Enter to continue...")
        elif choice == "4":
            PW_Manager.remove(UID, password)
            UI.prompt_text("Press Enter to continue...")
        elif choice.upper() == "B":
            break


def main_menu():
    UID = None
    password = None

    # PHASE 1: AUTHENTICATION PORTAL
    while UID is None:
        UI.clear_screen()
        UI.show_banner()
        UI.status_header()
        
        auth_choice = UI.menu(
            "Account Access Portal",
            [
                ("1", "📝 Register New User", "Create an account and receive an assigned 8-digit UID"),
                ("2", "🔑 Login", "Access your personal vault and security utilities"),
                ("3", "🚪 Exit Program", "Safely terminate the application")
            ],
            default="2"
        )

        if auth_choice == "1":
            UI.header("User Registration")
            result = User_Auth.register()
            if result:
                UI.prompt_text("Press Enter to proceed to login...")

        elif auth_choice == "2":
            UI.header("User Authentication")
            auth_result = User_Auth.login()
            if auth_result and auth_result[0] is not None:
                UID, password = auth_result
                Action_Hist.push_hist(f"[*] User logged in with UID: {UID}")
            else:
                UI.prompt_text("Press Enter to return...")

        elif auth_choice == "3" or auth_choice == "B":
            UI.info("Shutting down VantaCrypt suite. Stay safe!")
            Action_Hist.push_hist("[*] Program exited from authentication portal.")
            sys.exit(0)

    # PHASE 2: APPLICATION DASHBOARD
    while True:
        UI.clear_screen()
        UI.show_banner()
        vault_count = len(PW_Manager._load_vault(UID)) if hasattr(PW_Manager, '_load_vault') else None
        UI.status_header(actions_count=len(Action_Hist.history), vault_count=vault_count)

        choice = UI.menu(
            "Command Center — Main Tools",
            [
                ("1", "🛡️  Password Strength Checker", "Audit password entropy and receive hardening feedback"),
                ("2", "⚡  Password Generator", "Generate cryptographically randomized secure passwords"),
                ("3", "🔒  Encryption & Decryption Suite", "Multi-tiered XOR stream and shift ciphers"),
                ("4", "🔐  Password Vault Manager", "Secure credential storage, editing, and retrieval"),
                ("5", "📜  Session Action History", "Review chronological audit trail of all operations"),
                ("6", "📊  Security Graphs & Analytics", "Interactive statistics and security visualizations"),
                ("7", "🚪  Logout", "Lock vault and return to the authentication portal"),
                ("8", "❌  Exit", "Close the security suite")
            ],
            default="1"
        )

        if choice == "1":
            UI.clear_screen()
            UI.header("Password Strength Audit")
            Action_Hist.push_hist("[*] Opened Password Strength Checker.")
            PW_Strength.strength_test()
            UI.prompt_text("Press Enter to continue...")

        elif choice == "2":
            UI.clear_screen()
            UI.header("Cryptographic Password Generator")
            Action_Hist.push_hist("[*] Opened Password Generator.")
            PW_Generator.password_generator()
            UI.prompt_text("Press Enter to continue...")

        elif choice == "3":
            Action_Hist.push_hist("[*] Opened Encryption & Decryption Suite.")
            encryption_menu(UID)

        elif choice == "4":
            Action_Hist.push_hist("[*] Opened Password Vault Manager.")
            vault_menu(UID, password)

        elif choice == "5":
            UI.clear_screen()
            UI.header("Session Audit Log")
            Action_Hist.push_hist("[*] Viewed Session Action History.")
            Action_Hist.pull_hist()
            UI.prompt_text("Press Enter to continue...")

        elif choice == "6":
            UI.clear_screen()
            UI.header("Security Analytics & Graphs")
            Action_Hist.push_hist("[*] Viewed Security Analytics.")
            Graph.Graph()
            UI.prompt_text("Press Enter to continue...")

        elif choice == "7":
            UI.info("Logging out and securing workspace...")
            Action_Hist.push_hist(f"[*] User logged out (UID: {UID}).")
            UI.set_user(None, None)
            UID = None
            password = None
            break

        elif choice == "8" or choice == "B":
            UI.info("Closing VantaCrypt suite. Stay secure!")
            Action_Hist.push_hist("[*] Program exited from main menu.")
            sys.exit(0)


if __name__ == "__main__":
    while True:
        try:
            main_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            UI.warning("Session interrupted by user.")
            sys.exit(0)
