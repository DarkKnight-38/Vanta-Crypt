import sys
from InquirerPy import inquirer
from rich import print
import time

import Functions.Action_Hist as Action_Hist
import Functions.Encryptions as Encryptions
import Functions.Decryption as Decryption
import Functions.Graph as Graph
import Functions.PW_Generator as PW_Generator
import Functions.PW_Strength as PW_Strength
import Functions.User_Auth as User_Auth


def main_menu():
    UID = None
    password = None
    while UID is None:
        print("\n" + "="*29)
        print("  [purple4]Welcome to the VantaCrypt[/purple4]  ")
        print("="*29 + "\n")
        
        auth_choice = inquirer.select(
            message="Please select an option:",
            choices=[
                {"name": "Register", "value": "1"},
                {"name": "Login", "value": "2"},
                {"name": "Exit Program", "value": "3"}
            ],
            default="2"
        ).execute()
        
        if auth_choice == '1':
            result = User_Auth.register()
            if result is not False and result is not None:
                pass
                
        elif auth_choice == '2':
            CurrentUID, password = User_Auth.login()
            if CurrentUID is not False and CurrentUID is not None:
                UID = CurrentUID
                password = password

        elif auth_choice == '3':
            print("Exiting program...")
            Action_Hist.push_hist('[*] Program exited from authentication menu.')
            sys.exit() 


    print(f"\n[*] Loading tools...\n")
    
    while True:
        print()
        time.sleep(1)
        choice = inquirer.select(
            message="--- MAIN MENU --- What would you like to do?",
            choices=[
                {"name": "Password Strength Checker", "value": "1"},
                {"name": "Password Generator", "value": "2"},
                {"name": "Encryption/Decryption", "value": "3"},
                {"name": "Action History", "value": "4"},
                {"name": "Graphs", "value": "5"},
                {"name": "Password Manager", "value": "6"},
                {"name": "Logout", "value": "7"},
                {"name": "Exit", "value": "8"}
            ]
        ).execute()

        if choice == '1':
            if UID is None:
                print("[!] You must be logged in to use this.")
                continue
            print("Loading Password Strength Checker...")
            Action_Hist.push_hist('[*] Opened Password Strength Checker.')
            PW_Strength.strength_test()

        elif choice == '2':
            print("Loading Password Generator...")
            Action_Hist.push_hist('[*] Opened Password Generator.')
            PW_Generator.password_generator()

        elif choice == '3':
            enc_type = inquirer.select(
                message="Choose encryption level:",
                choices=[
                    {"name": "Minimum", "value": "min"},
                    {"name": "Intermediate", "value": "inter"},
                    {"name": "Maximum", "value": "max"}
                ]
            ).execute()
            
            if enc_type == 'min':
                print("Minimum encryption selected.")
                Action_Hist.push_hist('[*] Selected minimum encryption/decryption.')
                
                if inquirer.confirm(message="Do you want to encrypt a file?").execute():
                    text = inquirer.text(message="Enter the text to encrypt:").execute()
                    encrypted_file = inquirer.filepath(message="Enter the output .txt filename:").execute()
                    encryption_key_file = inquirer.filepath(message="Enter the output encryption key filename:").execute()
                    Encryptions.min_encrypt(encrypted_file, encryption_key_file, text, UID)
                                
                if inquirer.confirm(message="Do you want to decrypt a file?").execute():
                    encrypted_file = inquirer.filepath(message="Enter the .txt filename to decrypt:").execute()
                    encryption_key_file = inquirer.filepath(message="Enter the encryption key filename:").execute()
                    Decryption.min_decrypt(encrypted_file, encryption_key_file, UID)
                    
            elif enc_type == 'inter':
                Action_Hist.push_hist('[*] Selected intermediate encryption/decryption.')
                pass
                
            elif enc_type == 'max':
                print("Maximum encryption selected.")
                Action_Hist.push_hist('[*] Selected maximum encryption/decryption.')
                if inquirer.confirm(message="Do you want to encrypt a file?").execute():
                    text = inquirer.text(message="Enter the text to encrypt:").execute()
                    txt_file = inquirer.filepath(message="Enter the output .txt filename:").execute()
                    enc_key_file = inquirer.filepath(message="Enter the output encryption key filename:").execute()
                    Encryptions.max_encrypt(text, txt_file, enc_key_file, UID)
                                
                if inquirer.confirm(message="Do you want to decrypt a file?").execute():
                    txt_file = inquirer.filepath(message="Enter the .txt filename to decrypt:").execute()
                    enc_key_file = inquirer.filepath(message="Enter the encryption key filename:").execute()
                    Decryption.max_decrypt(txt_file, enc_key_file, UID)
                
        elif choice == '4':
            print("Loading Action History...")
            Action_Hist.push_hist('[*] Opened Action History.')
            Action_Hist.pull_hist()

        elif choice == '5':
            print("Loading Graphs...")
            Action_Hist.push_hist('[*] Opened Graphs.')

        elif choice == '6':
            print("Loading Password Manager...")
            Action_Hist.push_hist('[*] Opened Password Manager.')
            from Functions import PW_Manager
            while True:
                pm_choice = inquirer.select(
                    message="Password Manager - Choose an option:",
                    choices=[
                        {"name": "Add Entry", "value": "1"},
                        {"name": "Remove Entry", "value": "2"},
                        {"name": "Edit Entry", "value": "3"},
                        {"name": "View Entries", "value": "4"},
                        {"name": "Back to Main Menu", "value": "5"}
                    ]
                ).execute()

                if pm_choice == '1':
                    PW_Manager.add(UID)
                elif pm_choice == '2':
                    PW_Manager.remove(UID,password)
                elif pm_choice == '3':
                    PW_Manager.edit(UID,password)
                elif pm_choice == '4':
                    PW_Manager.view(UID,password)
                elif pm_choice == '5':
                    break
        elif choice == '7':
            print("Logging out...")
            Action_Hist.push_hist(f'[*] User logged out (UID: {UID}).')
            UID = None
            break

        elif choice == '8':
            print("Exiting the program...")
            Action_Hist.push_hist('[*] Program exited from main menu.')
            sys.exit()

if __name__ == "__main__":
    while True:
        main_menu()
