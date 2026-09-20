import csv
import os
import random
import pwinput

def login():
   from Main_UI import main_menu
   print("\n--- USER LOGIN ---")
   username = input('Enter your username: ').strip()
   password = pwinput.pwinput(prompt='Enter your password: ', mask='*').strip()
   if username == '' or password == '':
       print('[!] Username and password cannot be empty. Login aborted.')
       return main_menu()
   for row in csv.reader(open('Data\\UserData\\user_data.csv', 'r', newline='')):
       if row and row[0] == username and row[1] == password:
           print(f"Logging in as {username}...")
           print('[*] Login successful!')
           return row[2], row[1]
   print('[!] Invalid username or password. Login failed.')
   return main_menu()


def register():
    from Main_UI import main_menu
    print("\n--- USER REGISTRATION ---")
    username = input('Enter a username: ').strip()
    if username == '':
        print('[!] Username cannot be empty. Registration aborted.')
        return
    elif username.lower() == 'username':
        print('[!] "username" is not allowed as a username. Registration aborted.')
        return

    existing_users = []
    if os.path.exists('Data\\UserData\\user_data.csv'):
        with open('Data\\UserData\\user_data.csv', 'r', newline='') as g:
            data = csv.reader(g)
            for row in data:
                if row:  # Ensure the row isn't blank
                    existing_users.append(row[0])
                   
    if username in existing_users:
        print('[!] User already exists! Rerouting to main menu...')
        return main_menu()

  
    password = pwinput.pwinput(prompt='Enter a password: ', mask='*').strip()
    if password == '':
        print('[!] Password cannot be empty. Registration aborted.')
        return main_menu()

    attempts = 3
    re_password = pwinput.pwinput(prompt='Enter the password again: ', mask='*').strip()
   
 
    if password != re_password:
        print('[!] Re-Entered password is wrong. Registration failed. Please start over.')
        return main_menu()

    existing_ids = []
    f=open('Data\\UserData\\user_data.csv', 'r', newline='')
    for row in csv.reader(f):
        if row:  # Ensure the row isn't blank
            existing_ids.append(row[2])
    f.close()
    while True:
        unique_id = random.randint(10000000, 99999999)
        if unique_id not in existing_ids:
            existing_ids.append(unique_id)
            break
    
  
    with open('Data\\UserData\\user_data.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([username, password, unique_id])
       
    print('[*] User registered successfully!')