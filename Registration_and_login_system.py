#######################################################
# This program allows users to log in, register or delete theirs accounts.
# and stores their information in a JSON file. The storage
# system uses dictionaries, where the 'Usuarios'
# dictionary contains other dictionaries, each with a user
# name and password.
#######################################################

import json
import time

# This function reads user information from the JSON file.
def load_users():
    try:
        with open('Users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# This function saves login information to the JSON file.
def save_users(users):
    with open('Users.json', 'w') as f:
        json.dump(users, f)

# This function contains all the code responsible for the login process.
def login(users):
    username_valid = False
    tries = 0
    while not username_valid:
        username = input("Hello! Enter your username: ") 
        if (username not in users):
            print("The given username dont exist.")
            tries = tries+1
            if (tries == 3):
                print(f"\nThree incorrect entries. Do you want to register the user {username}?\n")
                option = input("Y: [Yes] N: [No]")
                if(option == 'Y'):
                    register_user(users, username, username_valid = True)
                elif(option != 'N'):
                    print("Invalid option.")
                    break
        else:
            username_valid = True
    
    password_valid = False
    while not password_valid:
        password = input(f"Hello, {username}! Please, enter your password: ")
        if(password != users[username]['Password']):
            print("Incorrect password. Try again.")
        else:
            print("Wait... Logging-in.")
            time.sleep(1)
            print(f"User {username} logged.")
            password_valid = True

# This function allows a new user to be registered.
def register_user(users, username, username_valid):
    while not username_valid:
        username = input("Please, enter a username: ")
        if(username in users):
            print("The chosed username alread exist. Try again")
        else:
            username_valid = True

    password_valid = False
    while not password_valid:
        password = input(f"Hello, {username}, enter a password: ")
        if (len(password) < 8):
            print("The password needs to have 8 or more characters.")
        else:
            print("Registering user. Please, wait...")
            time.sleep(2)
            users.update({username: {'User' : username, 'Password' : password}})
            save_users(users)
            print("User successful registered.")
            return

# This function allows a user to delete their account.
def delete_account(users):
    username_valid = False
    while not username_valid:
        username = input("Enter your username: ")
        if (username not in users):
            print("The given username dont exist. Try again...")
        else:
            username_valid = True
    
    password_valid = False
    while not password_valid:
        password = input("Enter your password: ")
        if (password != users[username]['Password']):
            print("Wrong password. Try again...")
        else:
            print("Deleting account. Please wait...")
            time.sleep(3)
            del(users[username])
            print("Account successful deleted.")
            save_users(users)
            password_valid = True

# This function allows a user to change your password.
def change_password(users):
    username_valid = False
    while not username_valid:
        name = input("To change your password, please enter your username: ")
        if name in users:
            username_valid = True
        else:
            print("Wrong username, please try again...")

    old_password_valid = False
    while not old_password_valid:
        old_password = int(input("Enter your old password: "))
        if (old_password == users[name]['Password']):
            old_password_valid = True
        else:
            print("Wrong password. Try again...")

    new_password_valid = False
    while not new_password_valid:
        new_password = int(input("Enter your new password: "))
        # aqui você pode adicionar outras verificações ou restrições para a nova senha
        if new_password == old_password:
            print("New password cannot be the same as the old password.")
        else:
            users[name]['password'] = new_password
            print("Password changed successfully!")
            save_users(users)
            break

# Main program
def main():
    users = load_users() # This code loads the JSON information into the "users" dictionary.
    options_menu = ''' Welcome to the options
    Enter '1' to log in
    Enter '2' to register a new user
    Enter '3' to delete your account
    Enter '4' to change your password
    '''
    option = input(options_menu)
    if(option == "1"):
        login(users)
    elif(option == "2"):
        register_user(users, username = None, username_valid = False)
    elif(option == "3"):
        delete_account(users)
    elif(option == '4'):
        change_password(users)
    else:
        print("Invalid option.")

main()