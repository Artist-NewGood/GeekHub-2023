import sqlite3
import os
import re
import random
from typing import Any
from time import sleep
from prettytable import PrettyTable
from datetime import datetime
from HT_12.ATM_version_4.main import verification_animation


class IncorrectLengthUsername(Exception):
    pass


class SpaceInUsername(Exception):
    pass


class IncorrectLengthUserPassword(Exception):
    pass


class NoDigitInPassword(Exception):
    pass


class NoUpperLettersInPassword(Exception):
    pass


class NoSpecificLettersInPassword(Exception):
    pass


def add_new_users() -> bool:
    """Adding a new user to a file"""

    print('\n**************************'
          '\nThe rule for registration:\n'
          ' - the username should not contain spaces and the length should be from 3 to 15 characters\n'
          ' - password must be at least 8 characters long\n'
          ' - the password must contain at least one digit, a capital letter and a special character\n'
          'P.S. If you change your mind and want to exit, press Enter\n')

    print('• Registration form •')

    username = validation_username('Create your username: ')
    password = validation_password('Create your password: ')

    if random.random() <= 0.1:
        welcome_bonus(username, password)
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

        print('Registration complete. Use your data for authorization')
        sleep(1)

        return True


def welcome_bonus(username: str, password: str) -> None:
    """"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()
    cursor.execute("""INSERT INTO users_balance ('login', 'balance')
                                  VALUES (?, ?)""",
                   (username, 100))
    db.commit()

    cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 'Amount', 'Date')
                                  VALUES (?, ?, ?, ?)""",
                   (username, 'Registration', '0', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()

    cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 'Amount', 'Balance_after', 'Date')
                                          VALUES (?, ?, ?, ?, ?)""",
                   (username, 'Welcome bonus', '100', '100', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.commit()

    cursor.execute("""INSERT INTO users ('login', 'password')
                                  VALUES (?, ?)""",
                   (username, password))
    db.commit()
    sleep(2)
    print('\nCongratulations.\n'
          'Today you were lucky enough to win a $100 deposit for registering.\n')
    sleep(1)
    print('Registration complete. Use your data for authorization')
    sleep(1)


def validation_username(prompt: str) -> str:
    """Checking the username for compliance with the requirements"""
    while True:
        username = input(prompt)
        try:
            if not username:
                sleep(1)
                print('❎ Cancel registration\n'
                      '\n♥ Bye ♥')
                exit()
            if not 3 <= len(username) <= 15:
                raise IncorrectLengthUsername(' ! Error, username is not the right length (need between 3 and 15)\n')
            if ' ' in username:
                raise SpaceInUsername(' ! Error, no spaces are allowed in the username\n')
        except IncorrectLengthUsername as error:
            verification_animation()
            sleep(1)
            print(error)
            continue
            # exit()
        except SpaceInUsername as error:
            verification_animation()
            sleep(1)
            print(error)
            continue
            # exit()

        verification_animation()
        print(' ✅ Good username')
        break
    return username


def check_username_exists(username: str) -> bool | str:
    """Checking the username for uniqueness"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT login
                            FROM users
                            WHERE login == ?""",
                       (username,))
        result = cursor.fetchone()

        if not result:
            return True

        print(' ❗ A user with this name already exists. Try again')
        exit()


def check_username_for_transfer(username: str) -> bool | str:
    """Checking the username for uniqueness"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT login
                            FROM users
                            WHERE login == ?""",
                       (username,))
        result = cursor.fetchone()

        if result:
            return True

        sleep(1)
        print(' ! Error, no user with that name found. Try again.\n')
        return False


def validation_password(prompt: str) -> bool | str:
    """Checking the password for compliance with the requirements"""
    while True:
        password = input(prompt)
        try:
            if not password:
                sleep(1)
                print('❎ Cancel registration\n'
                      '\n♥ Bye ♥')
                exit()
            if len(password) < 8:
                raise IncorrectLengthUserPassword(' ! Error, password is too short (must be more than 8 characters)\n')
            if password.isalpha():
                raise NoDigitInPassword(' ! Error, your password must contain at least one digit\n')
            if password == password.lower():
                raise NoUpperLettersInPassword(' ! Error, your password must contain at least one capital letter\n')
            if not re.sub(r'\w', '', password):
                raise NoSpecificLettersInPassword('! Error, your password must contain at least one specific letter\n')
        except IncorrectLengthUserPassword as error:
            verification_animation()
            sleep(1)
            print(error)
            continue

        except NoDigitInPassword as error:
            verification_animation()
            sleep(1)
            print(error)
            continue

        except NoUpperLettersInPassword as error:
            verification_animation()
            sleep(1)
            print(error)
            continue

        except NoSpecificLettersInPassword as error:
            verification_animation()
            sleep(1)
            print(error)
            continue

        verification_animation()
        print(' ✅ Good password')
        break
    return password


def show_transactions(username: str, option=1) -> list[Any]:
    """Viewing user transactions from a file as a formatted table"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()

        cursor.execute("""SELECT Operation, Amount, Balance_after, Date 
                            FROM users_transactions
                            WHERE login == ?""",
                       (username,))

        if option:
            data_operations = cursor.fetchall()

            table = PrettyTable()
            table.field_names = ['Operation', 'Amount', 'Balance_after', 'Date']

            for i in data_operations:
                table.add_row(i)

            print('\n***                     TRANSACTIONS                         ***')
            print(table)

        return data_operations


def add_transactions(username: str, funds: int, balance: int, operation: int) -> None:
    """Adding a user transaction to the end of a file"""

    operations = {1: 'Withdrawal', 2: 'Replenishment', 3: 'Deposit percents',
                  4: 'Sent a transfer', 5: 'Received a transfer'}

    full_path = check_file()
    if funds:
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 
                                                                      'Amount', 'Balance_after', 'Date')
                                VALUES (?, ?, ?, ?, ?)""",
                           (username, operations[operation], abs(funds),
                            balance + funds, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()


def check_login_data() -> str | bool:
    """Check user login data for presence in the file"""

    from HT_12.ATM_version_4.incasator.incasator_module import Incasator

    full_path = check_file()
    username = input('Enter your username: ')
    user_password = input('Enter your password: ')

    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT login, password
                            FROM users
                            WHERE login == ? and password == ?""",
                       (username, user_password))

        login = cursor.fetchone()

        if login == (username, user_password) and login != ('admin', 'admin'):
            verification_animation()
            print(' ✅ Login successful')
            sleep(1)
            return username

        elif login == ('admin', 'admin'):
            verification_animation()
            print(' ✅ Login successful')
            sleep(1)
            Incasator.incasator_menu(username)
            # return username

        verification_animation()
        print(' ! Error, username or password incorrect.')
        return False


def check_input_user_data(prompt: str) -> float | bool:
    """Checking user input values for type matching"""

    while True:
        try:
            number = input(prompt)
            if not number:
                return False
            return float(number)
        except ValueError:
            sleep(1)
            print(' ! Error, enter please a number\n')


def check_file() -> str:
    """Checking a file for existence on a given path"""

    full_path = os.path.join(os.getcwd(), 'ATM.db')

    try:
        with open(full_path, 'r') as db:
            return full_path
    except FileNotFoundError as error:
        print(error)
        exit()
