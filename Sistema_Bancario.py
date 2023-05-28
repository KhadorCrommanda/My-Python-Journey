import json
import time
from abc import ABC, abstractmethod

class User:
    def __init__(self, cpf, username, dob, address, password):
        self.cpf = cpf
        self.username = username
        self.dob = dob
        self.address = address
        self.password = password

class Accounts(ABC):
    def __init__(self, account_number, balance=0.0, cashouts=0, transactions= None):
        self.account_number = account_number
        self.balance = balance
        self.cashouts = cashouts
        self.transactions = transactions or []
    
    @abstractmethod
    def deposit(self, value, date):
        pass

    @abstractmethod
    def cashout(self, value, date):
        pass

    @abstractmethod
    def statement(self):
        pass

class Account(Accounts):
    def __init__(self, account_number, balance=0, cashouts=0, transactions=None):
        super().__init__(account_number, balance, cashouts, transactions)

    def deposit(self, value, date):
        if value <= 0:
            print('The deposit value cannot be negative.')
        else:
            self.balance += value
            transaction = {
                'Type': 'Deposit',
                'Value': str(value),
                'Date': date
            }
            self.transactions.append(transaction)
            print(f'Deposit of R$ {value:.2f} successful to account number {self.account_number}.')

    def cashout(self, value, date):
        if value <= 0:
            print('The cashout value cannot be negative.')
        elif value > 500:
            print('The withdrawal limit is R$ 500.00.')
        elif value > self.balance:
            print(f'Not enough balance. Your balance: R$ {self.balance}')
        elif self.cashouts >= 3:
            print('You have already made 3 withdrawals today. Please come back tomorrow.')
        else:
            transaction = {
                'Type': 'Cashout',
                'Value': str(value),
                'Date': date
            }
            self.transactions.append(transaction)
            self.balance -= value
            self.cashouts += 1
            print(f'Cashout of R$ {value} successful from account number {self.account_number}.')

    def statement(self):
        print(f"Bank Statement - Account Number: {self.account_number}")
        print("------------------------------")
        for transaction in self.transactions:
            print(f"Date: {transaction['Date']}")
            print(f"Moviment type: {transaction['Type']}")
            print(f"Value: {transaction['Value']}")
            print("------------------------------")

class Storage:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = f.read()
                if data:
                    return json.loads(data)
                else:
                    return {}
        except FileNotFoundError:
            with open(self.filename, 'w', encoding='utf-8') as f:
                return {}

    def save_data(self, users_data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4)

class CheckingAccount(Account):
    def __init__(self, account_number, balance=0.0, cashouts=0, transactions=None, overdraft_limit=500.0):
        super().__init__(account_number, balance, cashouts, transactions)
        self.overdraft_limit = overdraft_limit

    def cashout(self, value, date):
        if value > self.balance + self.overdraft_limit:
            print('Not enough balance and overdraft limit.')
        else:
            super().cashout(value, date)

class Bank:
    def __init__(self):
        self.users_data = {}
        self.storage = Storage('Users_data.json')

    def register_user(self):
        cpf_valid = False
        while not cpf_valid:
            cpf_set = set(self.users_data.keys())
            cpf = input('Hello! Enter your CPF [xxx.xxx.xxx-xx]: ')
            cpf = cpf.replace('.', '').replace('-', '')
            if (len(cpf) != 11 or not cpf.isdigit()):
                print('Invalid cpf. Try again...')
            else:
                if cpf in cpf_set:
                    print(f'The CPF {cpf} is already linked to an account.')
                else:
                    cpf_valid = True

        username = input('Please, enter your name: ')

        dob_valid = False
        while not dob_valid:
            dob = input('Enter your date of birth (xx/xx/xxxx): ')
            if (len(dob.replace('/', '')) != 8 or not dob.replace('/', '').isdigit()):
                print('Invalid date.')
            else:
                dob_valid = True

        logradouro = input('Enter your street: ')
        nro = input('Enter the number of your street: ')
        bairro = input('Enter the name of your district: ')
        cidade = input('Enter your city name: ')
        estado = input('Enter your state abbreviation: ')
        address = f"{logradouro}, {nro} - {bairro} - {cidade}/{estado}"

        password_valid = False
        while not password_valid:
            password = input('Enter a password: ')
            if len(password) < 8:
                print('The password needs to have 8 or more characters.')
            else:
                user = User(cpf, username, dob, address, password)
                self.users_data[cpf] = user.__dict__
                self.storage.save_data(self.users_data)
                print('User successfully registered.')
                password_valid = True

    def login(self):
        current_time = time.time()
        actual_date = time.strftime("%d/%m/%Y", time.localtime(current_time))

        cpf_valid = False
        while not cpf_valid:
            cpf = input('Enter your cpf: ')
            cpf = cpf.replace('.', '').replace('-', '')

            if (len(cpf) != 11 or not cpf.isdigit()):
                print('Invalid cpf.')
            elif cpf not in self.users_data:
                print('The given CPF is not linked to an account. Try again.')
            else:
                cpf_valid = True

        password_valid = False
        while not password_valid:
            password = input('Enter your password: ')
            if password != self.users_data[cpf]['password']:
                print('Wrong password. Try again... ')
            else:
                username = self.users_data[cpf]['username']
                print(f'User {username} logged.')
                break

        self.bank_main(actual_date, cpf)

    def create_account(self, cpf):
        user = self.users_data[cpf]
        if 'Accounts' in user:
            account_number = len(user['Accounts']) + 1
            user['Accounts'][account_number] = {
                'Bank_Agency': '0001',
                'Balance': 0.0,
                'Cashouts': 0,
                'Transactions': []
            }
            print(f'Account number {account_number} created for user {user["username"]}.')
            self.storage.save_data(self.users_data)
        else:
            user['Accounts'] = {
                1: {
                    'Bank_Agency': '0001',
                    'Balance': 0.0,
                    'Cashouts': 0,
                    'Transactions': []
                }
            }
            print(f'Account number 1 created for user {user["username"]}.')
            self.storage.save_data(self.users_data)

    def bank_main(self, actual_date, cpf):
        if 'Accounts' in self.users_data[cpf]:
            account_number = input('Enter the account number: ')
            if account_number in self.users_data[cpf]['Accounts']:
                account_data = self.users_data[cpf]['Accounts'][account_number]
                account = CheckingAccount(account_number, account_data['Balance'], account_data['Cashouts'],
                                          account_data['Transactions'])
            else:
                print(f'Account {account_number} does not exist.')

        else:
            print('You do not have an account yet. Let\'s create one for you.')
            self.create_account(cpf)

        while True:
            print('--------------------------------------')
            print('1 - Deposit')
            print('2 - Cashout')
            print('3 - Bank Statement')
            print('0 - Exit')
            option = input('Choose an option: ')

            if option == '1':
                value = float(input('Enter the deposit value: '))
                account.deposit(value, actual_date)

            elif option == '2':
                value = float(input('Enter the cashout value: '))
                account.cashout(value, actual_date)

            elif option == '3':
                account.statement()

            elif option == '0':
                break

        self.users_data[cpf]['Accounts'][account_number] = account.__dict__
        self.storage.save_data(self.users_data)
        print('Logged out.')
        exit()

    def run(self):
        self.users_data = self.storage.load_data()

        while True:
            print('--------------------------------------')
            print('1 - Register')
            print('2 - Login')
            print('0 - Exit')
            option = input('Choose an option: ')

            if option == '1':
                self.register_user()

            elif option == '2':
                self.login()

            elif option == '0':
                break

        print('Goodbye!')
        exit()

if __name__ == '__main__':
    bank = Bank()
    bank.run()