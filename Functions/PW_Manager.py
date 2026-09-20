from plistlib import UID

from Functions.Action_Hist import push_hist
from Functions.PW_Generator import password_generator
import pickle
import os

# These are placeholders for the password vault. They just log that they were opened.

def add(UID):
    file_name = 'Data\\PWManagerData\\password_vault_'+str(UID)+'.dat'
    data = []
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            
            while True:
                try:
                    data.append(pickle.load(f))
                except EOFError:
                    break
            
    push_hist('[*] Password manager add() was called.')
    details={'Website':'','Username':'','Password':'','Notes':'','UID':''}
    website = input("Enter the website: ")
    for entry in data:
        if entry['Website'] == website:
            print("[!] ERROR: This website already exists in the vault.")
            return
    username = input("Enter the username: ")
    password = input("Enter the password (Press Enter to generate a random password): ")
    if password == '':
        password = password_generator()
    notes = input("Enter any notes (optional): ")
    details['Website'] = website
    details['Username'] = username
    details['Password'] = password
    details['Notes'] = notes
    details['UID'] = UID
    f=open(file_name, 'ab')
    pickle.dump(details, f)
    f.close()
    push_hist(f"[*] Added new entry for website: {website} to the password vault.")


def remove(UID,password):
    push_hist('[*] Password manager remove() was called.')
    file_name = 'Data\\PWManagerData\\password_vault_'+str(UID)+'.dat'
    data = []
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
            
            while True:
                try:
                    data.append(pickle.load(f))
                except EOFError:
                    break
    password_input = input("Enter your password to remove an entry: ")
    if password_input != password:
        print("[!] ERROR: Incorrect password. Access denied.")
        push_hist('[!] ERROR: Incorrect password entered for removing an entry from the vault.')
        return
    else:
        print("[*] Access granted. You can now remove an entry from the password vault.")
        website = input("Enter the website to remove: ")
        flag= False
        for entry in data:
            if entry['Website'] == website:
                flag= True
                data.remove(entry)
                with open(file_name, 'wb') as f:
                    for entry in data:
                        pickle.dump(entry, f)
                print(f"[*] Removed entry for website: {website} from the password vault.")
                push_hist(f"[*] Removed entry for website: {website} from the password vault.")
                return
        if not flag:
            print(f"[!] ERROR: No entry found for website: {website}.")
            push_hist(f"[!] ERROR: No entry found for website: {website} to remove from the vault.")
def edit(UID,password):
    push_hist('[*] Password manager edit() was called.')
    pass

def view(UID, password):
    push_hist('[*] Password manager view() was called.')
    file_name = 'Data\\PWManagerData\\password_vault_'+str(UID)+'.dat'
    data = []
    if os.path.exists(file_name):
        with open(file_name, 'rb') as f:
                
            while True:
                try:
                    data.append(pickle.load(f))
                except EOFError:
                    break
    password_input = input("Enter your password to view the vault: ")
    if password_input != password:
        print("[!] ERROR: Incorrect password. Access denied.")
        push_hist('[!] ERROR: Incorrect password entered for viewing the vault.')
        return
    else:
        print("[*] Access granted. Displaying password vault entries:")
        for entry in data:
            print(f"Website: {entry['Website']}")
            print(f"Username: {entry['Username']}")
            print(f"Password: {entry['Password']}")
            print(f"Notes: {entry['Notes']}")
            print("-" * 30)
            print()
    