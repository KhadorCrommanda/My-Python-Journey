#######################################################
# This program allows users to log in, register or delete theirs accounts.
# and stores their information in a JSON file. The storage
# system uses dictionaries, where the 'Usuarios'
# dictionary contains other dictionaries, each with a user
# name and password.
#######################################################

import json

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
    while True:
        name = input("Hello, please enter your username: ")
        if (name in users):
            password = int(input(f"Welcome back, {name}! Please enter your password: "))
            if (password == users[name]["Password"]):
                print(f"Access granted for user '{name}'.")
                return # Ends the login() function successfully
            else:
                print("Incorrect password, please try again.")
        else:
            print("Username not found.")
            option = input("Enter '1' to try again or '2' to register a new user: ")
            if option == "2":
                register_user(users)
            elif option != "1":
                print("Invalid option, exiting program.")
                return # Ends the login() function with failure

# This function allows a new user to be registered.
def register_user(users):
    while True:
        name = input("Enter a username: ")
        if(name in users):
            print("This username already exists, please try another one.")
            continue
            # If the username already exists, the user is prompted to enter another name.
        else:
            try:
                password = int(input("Enter a password: "))
            except:
                print("Error 0x1: Your password probably contains letters (only numbers are allowed).")
                # If the password contains letters instead of numbers, the user is prompted to enter another password.
            else:
                users[name] = {"User": name, "Password": password} # If the chosen username and password are valid, a new user is registered.
                print(f"User '{name}' registered successfully!")
                save_users(users)
                return

# This function allows a user to delete their account.
def delete_account(users):
    while True:
        name = input("Please enter your username: ")
        if(name in users.keys()):
            password = int(input("Please enter your account password: "))
            if(password == users[name]["Password"]):
                print("Deleting account from the system...\n")
                del users[name]            
                print("Account deleted successfully.")
                save_users(users)
                return
            else:
                print("Incorrect password, please try again.")
        else:
            print("User not found.")

# Main program
def main():
    users = load_users() # This code loads the JSON information into the "users" dictionary.
    options_menu = ''' Welcome to the options
    Enter '1' to log in
    Enter '2' to register a new user
    Enter '3' to delete your account
    '''
    option = input(options_menu)
    if(option == "1"):
        login(users)
    elif(option == "2"):
        register_user(users)
    elif(option == "3"):
        delete_account(users)
    else:
        print("Invalid option.")

main()