# Write your code here
import random
import sqlite3


class BankAccount:
    IIN = 400000
    N_CARDS = 0

    def __init__(self, connection):
        self._pin, self.account_number, self.id_bank_account = None, None, None
        self.balance = 0
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS card (
                  id INTEGER,
                  number TEXT,
                  pin TEXT,
                  balance INTEGER DEFAULT 0);
                  """)
        self.connection.commit()
        self.welcome()

    def welcome(self):
        print("""
        1. Create an account
        2. Log into account
        0. Exit""")
        inp = input()
        if inp == '1':
            return self.create_account()
        elif inp == '2':
            return self.login()
        elif inp == '0':
            BankAccount._exit()
        else:
            print('Wrong input')
            return self.welcome()

    def create_account(self):
        account_number = self.gen_card_number()
        print('Your card has been created')
        print('Your card number:')
        print(account_number)
        pin = str(random.randint(0, 9999)).rjust(4, '0')
        print('Your card PIN:')
        print(pin)
        balance = 0
        self._number_reg(account_number, pin, balance)
        return self.welcome()

    def _number_reg(self, account_number, pin, balance):
        try:
            self.cursor.execute(F"""
                INSERT INTO card (id, number, pin, balance)
                VALUES ({self.N_CARDS}, {account_number}, '{str(pin)}', {balance})         
            """)
            self.N_CARDS += 1
            self.connection.commit()
        except sqlite3.OperationalError:
            print('An error occurred while trying to insert record into DB')
        return None

    def gen_card_number(self):
        inn = str(self.IIN)
        acn = str(random.randint(0, 999999999)).rjust(9, '0')
        cin = self.generate_cin(inn+acn)
        return inn+acn+cin

    @staticmethod
    def generate_cin(account_id):
        temp_number = list(map(int, list(account_id)))
        for i, n in enumerate(temp_number, start=1):
            if i % 2 != 0:
                temp_number[i-1] = temp_number[i - 1] * 2 - 9 if (temp_number[i - 1] * 2) > 9 else temp_number[i - 1] * 2
        cin = 10 - sum(temp_number) % 10 if sum(temp_number) % 10 != 0 else 0
        return str(cin)

    def check_cin(self, number):
        return number[-1] == self.generate_cin(number[0:len(number)-1])

    def login(self):
        input_card_number = input('Enter your card number:\n')
        try:
            assert self.check_cin(input_card_number), "Probably you made a mistake in the card number. Please try again!"
            input_pin = input('Enter your PIN\n')
            self.cursor.execute(f'SELECT * FROM card WHERE number == {input_card_number}')
            bank_account_data = self.cursor.fetchone()
            print(bank_account_data)
            self.id_bank_account = bank_account_data[0]
            repr(self.id_bank_account)
            self.account_number = bank_account_data[1]
            assert input_card_number == self.account_number, "Such a card does not exist."
            self._pin = bank_account_data[2]
            assert input_pin == self._pin, "Wrong Pin"
            print('You have successfully logged in!\n')
            self.balance = bank_account_data[3]
            self.connection.commit()
            self.login_menu()
        except AssertionError as e_assert:
            print(e_assert)
            return self.welcome()

    def login_menu(self):
        print("""
        1. Balance
        2. Add income
        3. Do transfer
        4. Close account
        5. Log out
        0. Exit""")
        login_choice = input()
        if login_choice == '1':
            return self.print_balance()
        elif login_choice == '2':
            return self.add_income()
        elif login_choice == '3':
            return self.do_transfer()
        elif login_choice == '4':
            return self.close_account()
        elif login_choice == '5':
            print('You have successfully logged out!')
            return self.welcome()
        elif login_choice == '0':
            return self._exit()
        else:
            print('Wrong input, try again: \n')
            return self.login_menu()

    def print_balance(self):
        print(f'Balance: {self.balance}')
        return self.login_menu()

    def add_income(self):
        income_to_add = int(input('Enter income: \n'))
        self.balance += income_to_add
        try:
            self.cursor.execute(f"UPDATE card SET balance = {self.balance} WHERE id = {self.id_bank_account}")
            print('Income was added!')
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print('Error while updating balance, try again ', e)
            return self.login_menu()
        return self.login_menu()

    def do_transfer(self):
        print('Transfer')
        destination_number = input('Enter card number: \n')
        try:
            assert self.check_cin(destination_number), "Probably you made a mistake in the card number. Please try again!"
            assert destination_number != self.account_number, "You can't transfer money to the same account!"
            self.cursor.execute(f'SELECT * FROM card WHERE number = {destination_number}')
            data = self.cursor.fetchone()
            assert data, "Such a card does not exist."
            destination_id = data[0]
            destination_balance = data[3]
            money_transfer = int(input('Enter how much money you want to transfer: \n'))
            assert money_transfer <= self.balance, "Not enough money!"
            destination_balance += money_transfer
            self.balance -= money_transfer
            self.cursor.execute(f'UPDATE card SET balance = {destination_balance} WHERE id = {destination_id}')
            self.cursor.execute(f'UPDATE card SET balance = {self.balance} WHERE id = {self.id_bank_account}')
            print('Success!')
            self.connection.commit()
            return self.login_menu()
        except AssertionError as e:
            print(e)
            return self.login_menu()
        except sqlite3.OperationalError:
            print('An error occurred while transferring money')
            return self.login_menu()

    def close_account(self):
        try:
            print(self.id_bank_account)
            self.cursor.execute(f'DELETE FROM card WHERE id = {self.id_bank_account}')
            print('The account has been closed!')
            self.connection.commit()
            return self.welcome()
        except sqlite3.OperationalError:
            print('An error occurred while closing the account.')
            return self.login_menu()

    @staticmethod
    def _exit():
        exit('Bye')


with sqlite3.connect('card.s3db') as conn:
    BankAccount(connection=conn)
