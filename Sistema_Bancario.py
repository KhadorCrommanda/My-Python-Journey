##################################################################
#Sistema bancario feito por KhadorCrommanda.
#O script criará um arquivo chamado users_data
#serve para armazenar todos os usuarios e seus movimentos financeiros.
##################################################################
# -*- coding: utf-8 -*-

import json
import time

def  load_data():
    try:
        with open('Users_data.json', 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return {}
    except FileNotFoundError:
        with open('Users_data.json', 'w', encoding='utf-8') as f:
            return {}
def save_data(users_data):
    with open('Users_data.json', 'w', encoding='utf-8') as f:
        json.dump(users_data, f, ensure_ascii=False, indent=4)

def register_user(users_data):
    cpf_valid = False
    while not cpf_valid:
        cpf_set = set(users_data.keys())
        cpf = input('Hello! Enter your CPF [xxx.xxx.xxx-xx]: ')
        cpf = cpf.replace('.', '').replace('-', '')
        if (len(cpf) != 11 or not cpf.isdigit()):
            print('Invalid cpf. Try again...')
        else:
            if cpf in cpf_set:
                print(f'The CPF {cpf} is already linked to an account.')
            else:
                cpf_valid = True
    
    username_valid = False
    while not username_valid:
        username = input('Please, enter your name: ')
        username_valid = True

    DoB_valid = False
    while not DoB_valid:
        DoB = input('Enter your date of birth (xx/xx/xxxx): ')
        if (len(DoB.replace('/', '')) != 8 or not DoB.replace('/', '').isdigit()):
            print('Invalid date.')
        else:
            DoB_valid = True
    
    address_valid = False
    while not address_valid:
        logradouro = input('Enter your street: ')
        nro = input('Enter the number of your street: ')
        bairro = input('Enter the name of your district: ')
        cidade = input('Enter your city name: ')
        estado = input('Enter your state abbreviation: ')
        address = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}"

        print(f'your address is {address}. Is everything right? [Y] to Yes, [N] to No')
        option = input()
        if (option == 'Y' or 'y'):
            address_valid = True
        elif (option != 'N' or 'n'):
            print('invalid option.')
     
    password_valid = False
    while not password_valid:
        password = input('Enter a password: ')
        if (len(password) < 8):
            print('The password needs to have 8 or more characters.')
        else:
            users_data.update({cpf:{'Username' : username, 'Password' : password, 'Address' : address, 'Date_of_birth' : DoB}})
            save_data(users_data)
            print('User successful registered.')
            password_valid = True

def login(users_data):
    current_time = time.time()
    actual_date = time.strftime("%d/%m/%Y", time.localtime(current_time))

    cpf_valid = False
    while not cpf_valid:
        cpf = input('Enter your cpf: ')
        cpf = cpf.replace('.', '').replace('-', '')
        
        if (len(cpf) != 11 or not cpf.isdigit()):
            print('invalid cpf.')
        elif cpf not in users_data:
            print('The given CPF is not linked to an account. Try again.')
        else:
            cpf_valid = True
    
    password_valid = False
    while not password_valid:
        password = input('Enter your password: ')
        if (password != users_data[cpf]['Password']):
            print('Wrong password. Try again... ')
        else:
            username = users_data[cpf]['Username']
            print(f'User {username} logged.')
            break

    def create_account():
        if ('Accounts' in users_data[cpf]):
            account_number = len(users_data[cpf]['Accounts']) + 1
            users_data[cpf].update({
            'Accounts':{ account_number: {
            'Bank_Agency': '0001',
            'Balance': 0.00,
            'Cashouts': 0,
            'Transactions': []
            }}})

            print(f'Account number {account_number} created for user {username}.')
            save_data(users_data)
        else:
            users_data[cpf].update({
            'Accounts':{ 1: {
            'Bank_Agency': '0001',
            'Balance': 0.00,
            'Cashouts': 0,
            'Transactions': []
            }}})
            print(f"Account number '1' created for user {username}.")
            save_data(users_data)

    def deposit(actual_date):
        deposit_valid = False     
        while not deposit_valid:
            destiny = input('Enter the number of the destination account: ')
            if destiny not in users_data[cpf]['Accounts']:
                print('The destination account does not exist. Try again.')
            else:
                account = users_data[cpf]['Accounts'][destiny]
                balance = account['Balance']

                value = float(input('Enter the value of the deposit: '))
                if value <= 0:
                    print('The deposit value cannot be negative.')
                else:
                    account['Balance'] = float(balance + value)
                    transaction = {
                    'Type': 'Deposit',
                    'Value': str(value),
                    'Date': actual_date
                }
                    account['Transactions'].append(transaction)
                    save_data(users_data)
                    print(f'Deposit of R$ {value:.2f} successful to account number {destiny}.')
                    deposit_valid = True

    def cashout(actual_date = time.strftime("%d/%m/%Y", time.localtime(current_time))):
        cashout_valid = False
        while not cashout_valid:
            number = input('Enter the account number from which the money will be withdrawn: ')
            if number not in users_data[cpf]['Accounts']:
                print('The given account number does not exist.')
            elif not number.isdigit():
                print('Invalid account number.')
            else:
                account = users_data[cpf]['Accounts'][number]
                balance = account['Balance']
                cashouts = account.get('Cashouts', 0)  # Obter o número de saques ou 0 se não existir

                value = float(input('Enter the cashout value: '))
                if value <= 0:
                    print('The cashout value cannot be negative.')
                elif value > 500:
                    print('The withdrawal limit is R$ 500.00.')
                elif value > balance:
                    print(f'Not enough balance. Your balance: R$ {balance}')
                elif cashouts >= 3:
                    print('You have already made 3 withdrawals today. Please come back tomorrow.')
                    break
                else:
                    transaction = {
                    'Type': 'Cashout',
                    'Value': str(value),
                    'Date': actual_date
                }
                    account['Transactions'].append(transaction)
                    account['Balance'] = float(balance - value)
                    users_data[cpf]['Accounts'][number]['Cashouts'] = cashouts + 1
                    save_data(users_data)
                    print(f'Cashout of R$ {value} successful from account number {number}.')
                    cashout_valid = True

    def statement():
        account_number = input('Enter the account number: ')
        if account_number not in users_data[cpf]['Accounts']:
            print('The account number does not exist.')
            return
    
        account = users_data[cpf]['Accounts'][account_number]
        transactions = account['Transactions']
        
        print(f"Bank Statement - Account Number: {account_number}")
        print("------------------------------")
        
        for transaction in transactions:
            date = transaction['Date']
            tipo = transaction['Type']
            amount = transaction['Value']
            print(f"Date: {date}")
            print(f"Moviment type: {tipo}")
            print(f"Value: {amount}")
            print("------------------------------")

    def bank_main(actual_date):
        menu = """
        Enter [C] to create a new bank account
        Enter [D] to make a deposit.
        Enter [S] to make a cashout
        Enter [H] to show your Bank Statement
        Enter [Q] to Quit.
        """
        option = input(menu)
        if option.lower() == 'c':
            create_account()
        elif option.lower() == 'd':
            deposit(actual_date)
        elif option.lower() == 's':
            cashout()
        elif option.lower() == 'h':
            statement()
        elif option.lower() == 'q':
            exit()
        else:
            print('Invalid option.')
    bank_main(actual_date)

def main():
    users_data = load_data()
    menu = """
    Enter [R] to register
    Enter [L] to login
    Enter [Q] to Exit program.
    """
    option = input(menu)
    if option.lower() == 'r':
        register_user(users_data)
    elif option.lower() == 'l':
        login(users_data)
    elif option.lower() == 'q':
        exit()
    else:
        print('Invalid option.')

main()