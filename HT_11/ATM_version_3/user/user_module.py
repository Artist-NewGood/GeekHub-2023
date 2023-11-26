import sqlite3
import os
import re
import random
from time import sleep
from datetime import datetime
from typing import Any
from prettytable import PrettyTable
from HT_11.ATM_version_3.atm.atm_module import Atm
from HT_11.ATM_version_3.incasator.incasator_module import Incasator
from HT_11.ATM_version_3.main import sub_menu, verification_animation
from HT_11.ATM_version_3.system.system_module import (check_file, check_input_user_data,
                                                      validation_password, validation_username)


# class IncorrectLengthUsername(Exception):
#     pass
#
#
# class SpaceInUsername(Exception):
#     pass
#
#
# class IncorrectLengthUserPassword(Exception):
#     pass
#
#
# class NoDigitInPassword(Exception):
#     pass
#
#
# class NoUpperLettersInPassword(Exception):
#     pass
#
#
# class NoSpecificLettersInPassword(Exception):
#     pass


class User:
    def __init__(self, username, money_request, password, funds, balance, option):
        self.username = username
        # self.money_request = money_request
        # self.password = password
        # self.funds = funds
        # self.balance = balance
        # self.option = option

    # @staticmethod
    def show_balance(self: str) -> int:
        """View the user's balance"""

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT balance
                              FROM users_balance
                              WHERE login == ?""",
                           (self,))

            result, *_ = cursor.fetchone()
            return result

    # @staticmethod
    def change_balance(self: str, money_request=None) -> None | bool:
        """Updates the user's balance in the database after a withdrawal or replenishment operation"""

        amount_balance = User.show_balance(self)
        full_path = check_file()
        if amount_balance + money_request >= 0:
            with sqlite3.connect(full_path) as db:
                cursor = db.cursor()
                cursor.execute("""UPDATE users_balance
                                  SET balance = ?
                                  WHERE login == ?""",
                               (amount_balance + money_request, self))

                print('✅ Complete operation')
                return True
        sleep(1)
        sub_menu(self)

    @staticmethod
    def withdrawal(username: str) -> None:
        """It allows withdrawing funds from the user's balance,
           as well as handles options when the user has no money on the balance or the ATM itself has no money"""

        total_amount_money_in_atm = sum(number[0] * number[1] for number in Atm.balance_atm('sum'))
        if not total_amount_money_in_atm:
            sleep(1)
            print('We are sorry, but there is no money in the ATM at the moment.\n'
                  'Try again later or write to us at fildaiko@gmail.com to speed '
                  'up the replenishment of the ATM by a cashier.')
            sleep(1)
            sub_menu(username)

        amount_balance = User.show_balance(username)
        if not amount_balance:
            sleep(1)
            print(f'\nThe withdrawal operation is not available because your balance is {amount_balance}$.\n'
                  f'Replenishment money first.')
            sub_menu(username)

        minimum_multiplicity_of_withdrawal, *_ = min(Atm.balance_atm('withdrawal'), key=lambda banknote: banknote[0])
        sleep(1)
        print(f'Now in your balance: {amount_balance}$\n'
              f'Minimum multiplicity of withdrawal: {minimum_multiplicity_of_withdrawal}$')

        while True:
            money_withdrawal = int(check_input_user_data('How much money you want to withdrawal '
                                                         '(or press "Enter" to cancel)?: '))
            if not money_withdrawal:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)
            if money_withdrawal < 0:
                sleep(1)
                print(' ! Error, the amount cannot be negative.\n')
                continue
            if money_withdrawal % minimum_multiplicity_of_withdrawal:
                sleep(1)
                print('! Error, amount does not meet the minimum multiplicity, try again\n')
                sleep(1)
                continue

            if money_withdrawal > total_amount_money_in_atm:
                sleep(1)
                print(
                    '! Error, amount of the withdrawal is more than the money in ATM, please enter a smaller amount\n')
                sleep(1)
                continue

            if money_withdrawal > amount_balance:
                sleep(1)
                print(f'\nError, the withdrawal amount is higher than the amount available on the account.'
                      f'\n!Your balance is {amount_balance}$\n'
                      f'Enter a smaller amount\n')
                sleep(1)
                continue

            break

        if User.change_balance(username, -money_withdrawal):
            User.add_transactions(username, -money_withdrawal, amount_balance)
            sleep(1)
            sub_menu(username)

    # @staticmethod
    def replenishment_money(self: str) -> None:
        """Allows the user to replenish their balance in an amount that is a multiple of the minimum
            face value of the atm banknote. Part of the money will also be returned to the user if the
            replenishment amount is not a multiple of the minimum face value."""

        amount_balance = User.show_balance(self)

        minimum_multiplicity_of_replenishment, *_ = min(Atm.balance_atm('replenishment'),
                                                        key=lambda banknote: banknote[0])
        sleep(1)
        print(f'Minimum multiplicity of replenishment: {minimum_multiplicity_of_replenishment}$')

        while True:
            money_replenishment = float(check_input_user_data('How much money you want to replenishment '
                                                              '(or press "Enter" to cancel)?: '))
            if not money_replenishment:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(self)
            if money_replenishment < 0:
                sleep(1)
                print(' ! Error, the amount cannot be negative.\n')
                continue

            if money_replenishment < minimum_multiplicity_of_replenishment:
                sleep(1)
                print('! Error, amount does not meet the minimum multiplicity, try again\n')
                sleep(1)
                continue

            final_money_replenishment = (money_replenishment -
                                         (money_replenishment % minimum_multiplicity_of_replenishment))

            if money_replenishment % minimum_multiplicity_of_replenishment:
                print(f'The amount {money_replenishment % minimum_multiplicity_of_replenishment}$ was not credited '
                      f'to the account and was returned to you')

            User.change_balance(self, abs(final_money_replenishment))
            User.add_transactions(self, int(abs(final_money_replenishment)), amount_balance)
            sleep(1)
            sub_menu(self)

    @staticmethod
    def add_new_users() -> bool:
        """Adding a new user to a database"""

        print('\n**************************'
              '\nThe rule for registration:\n'
              ' - the username should not contain spaces and the length should be from 3 to 15 characters\n'
              ' - password must be at least 8 characters long\n'
              ' - the password must contain at least one digit, a capital letter and a special character\n'
              'P.S. If you change your mind and want to exit, press Enter\n'
              '\nP.P.S.🔥 !!! A promotion for new users. 10% chance to win a $100 deposit\n')

        print('• Registration form •')

        username = validation_username(input('Create your username: '))
        password = validation_password(input('Create your password: '))

        chance = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        if chance == 1:
            User.welcome_bonus(username, password)
            return True

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO users_balance ('login', 'balance')
                              VALUES (?, ?)""",
                           (username, '0'))
            db.commit()

            cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 'Amount', 'Date')
                              VALUES (?, ?, ?, ?)""",
                           (username, 'Registration', '0', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()

            cursor.execute("""INSERT INTO users ('login', 'password')
                              VALUES (?, ?)""",
                           (username, password))
            db.commit()
            sleep(2)
            print('\nUnfortunately!.\n'
                  'Today you were not lucky. But we are still glad to welcome you to our ATM.\n')
            sleep(1)
            print('Registration complete. Use your data for authorization')
            sleep(1)

            return True

    # @staticmethod
    def welcome_bonus(self: str, password: str) -> None:
        """"""

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
        cursor.execute("""INSERT INTO users_balance ('login', 'balance')
                                      VALUES (?, ?)""",
                       (self, 100))
        db.commit()

        cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 'Amount', 'Date')
                                      VALUES (?, ?, ?, ?)""",
                       (self, 'Registration', '0', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()

        cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 'Amount', 'Balance_after', 'Date')
                                              VALUES (?, ?, ?, ?, ?)""",
                       (self, 'Welcome bonus', '100', '100', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.commit()

        cursor.execute("""INSERT INTO users ('login', 'password')
                                      VALUES (?, ?)""",
                       (self, password))
        db.commit()
        sleep(2)
        print('\nCongratulations.\n'
              'Today you were lucky enough to win a $100 deposit for registering.\n')
        sleep(1)
        print('Registration complete. Use your data for authorization')
        sleep(1)

    #
    # @staticmethod
    # def validation_username(username) -> str:
    #     """Checking the username for compliance with the requirements"""
    #
    #     try:
    #         if not username:
    #             print('❎ Cancel registration\n'
    #                   '\n♥ Bye ♥')
    #             exit()
    #         if not 3 <= len(username) <= 15:
    #             raise IncorrectLengthUsername(' ! Error, username is not the right length '
    #                                           '(need length between 3 and 15)')
    #         if ' ' in username:
    #             raise SpaceInUsername(' ! Error, no spaces are allowed in the username')
    #     except IncorrectLengthUsername as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #     except SpaceInUsername as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #
    #     verification_animation()
    #     User.check_username_exists(username)
    #     print(' ✅ Good username')
    #
    #     return username
    #
    # @staticmethod
    # def check_username_exists(username: str) -> bool:
    #     """Checking the username for uniqueness"""
    #
    #     full_path = User.check_file()
    #     with sqlite3.connect(full_path) as db:
    #         cursor = db.cursor()
    #         cursor.execute("""SELECT login
    #                           FROM users
    #                           WHERE login == ?""",
    #                        (username,))
    #         result = cursor.fetchone()
    #
    #         if not result:
    #             return True
    #
    #         print(' ❗ A user with this name already exists. Try again')
    #         exit()
    #
    # @staticmethod
    # def validation_password(password: str) -> bool | str:
    #     """Checking the password for compliance with the requirements"""
    #
    #     try:
    #         if not password:
    #             print('❎ Cancel registration\n'
    #                   '\n♥ Bye ♥')
    #             exit()
    #         if len(password) < 8:
    #             raise IncorrectLengthUserPassword(' ! Error, your password is too short '
    #                                               '(must be more than 8 characters)')
    #         if password.isalpha():
    #             raise NoDigitInPassword(' ! Error, your password must contain at least one digit')
    #         if password == password.lower():
    #             raise NoUpperLettersInPassword(' ! Error, your password must contain at least one capital letter')
    #         if not re.sub(r'\w', '', password):
    #             raise NoSpecificLettersInPassword('! Error, your password must contain at least one specific letter')
    #     except IncorrectLengthUserPassword as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #     except NoDigitInPassword as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #     except NoUpperLettersInPassword as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #     except NoSpecificLettersInPassword as error:
    #         verification_animation()
    #         print(error)
    #         exit()
    #
    #     verification_animation()
    #     print(' ✅ Good password')
    #     return password

    # @staticmethod
    def show_transactions(self: str, option: object = 1) -> list[Any]:
        """Viewing user transactions from a database as a formatted table"""

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()

            cursor.execute("""SELECT Operation, Amount, Balance_after, Date 
                              FROM users_transactions
                              WHERE login == ?""",
                           (self,))

            if option:
                data_operations = cursor.fetchall()

                table = PrettyTable()
                table.field_names = ['Operation', 'Amount', 'Balance_after', 'Date']

                for i in data_operations:
                    table.add_row(i)

                print('\n***                     TRANSACTIONS                         ***')
                print(table)

            return data_operations

    # @staticmethod
    def add_transactions(self: str, funds: int, balance: int) -> None:
        """Adding a user transaction to the appropriate table in the database"""

        full_path = check_file()
        if funds:
            with sqlite3.connect(full_path) as db:
                cursor = db.cursor()
                cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 
                                                                        'Amount', 'Balance_after', 'Date')
                                  VALUES (?, ?, ?, ?, ?)""",
                               (self, "Withdrawal" if funds < 0 else "Replenishment", abs(funds),
                                balance + funds, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                db.commit()

    # @staticmethod
    # def check_login_data() -> str | bool:
    #     """Check for user login information in the database"""
    #
    #     full_path = User.check_file()
    #     username = input('Enter your username: ')
    #     user_password = input('Enter your password: ')
    #
    #     with sqlite3.connect(full_path) as db:
    #         cursor = db.cursor()
    #         cursor.execute("""SELECT login, password
    #                           FROM users
    #                           WHERE login == ? and password == ?""",
    #                        (username, user_password))
    #
    #         login = cursor.fetchone()
    #
    #         if login == (username, user_password) and login != ('admin', 'admin'):
    #             verification_animation()
    #             print(' ✅ Login successful')
    #             sleep(1)
    #             return username
    #
    #         elif login == ('admin', 'admin'):
    #             verification_animation()
    #             print(' ✅ Login successful')
    #             sleep(1)
    #             Incasator.incasator_menu(username)
    #             # return username
    #
    #         verification_animation()
    #         print(' ! Error, username or password incorrect.')
    #         return False
    #
    # @staticmethod
    # def check_input_user_data(prompt: str) -> float | bool:
    #     """Checking user input values for type matching"""
    #
    #     while True:
    #         try:
    #             number = input(prompt)
    #             if not number:
    #                 return False
    #             return float(number)
    #         except ValueError:
    #             sleep(1)
    #             print(' ! Error, enter please a number\n')
    #
    # @staticmethod
    # def check_file() -> str:
    #     """Checking a file for existence on a given path"""
    #
    #     full_path = os.path.join(os.getcwd(), 'ATM.db')
    #
    #     try:
    #         with open(full_path, 'r') as db:
    #             return full_path
    #     except FileNotFoundError as error:
    #         print(error)
    #         exit()
