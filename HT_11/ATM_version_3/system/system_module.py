import os
import sqlite3
import re
from time import sleep
from HT_11.ATM_version_3.main import verification_animation
from HT_11.ATM_version_3.incasator.incasator_module import Incasator


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


class IncorrectDenominationBanknote(Exception):
    pass


class IncorrectNumberBanknotesWithdrawal(Exception):
    pass


def check_login_data() -> str | bool:
    """Check for user login information in the database"""

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


def validation_username(username) -> str:
    """Checking the username for compliance with the requirements"""

    try:
        if not username:
            print('❎ Cancel registration\n'
                  '\n♥ Bye ♥')
            exit()
        if not 3 <= len(username) <= 15:
            raise IncorrectLengthUsername(' ! Error, username is not the right length '
                                          '(need length between 3 and 15)')
        if ' ' in username:
            raise SpaceInUsername(' ! Error, no spaces are allowed in the username')
    except IncorrectLengthUsername as error:
        verification_animation()
        print(error)
        exit()
    except SpaceInUsername as error:
        verification_animation()
        print(error)
        exit()

    verification_animation()
    check_username_exists(username)
    print(' ✅ Good username')

    return username


def check_username_exists(username: str) -> bool:
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


def validation_password(password: str) -> bool | str:
    """Checking the password for compliance with the requirements"""

    try:
        if not password:
            print('❎ Cancel registration\n'
                  '\n♥ Bye ♥')
            exit()
        if len(password) < 8:
            raise IncorrectLengthUserPassword(' ! Error, your password is too short '
                                              '(must be more than 8 characters)')
        if password.isalpha():
            raise NoDigitInPassword(' ! Error, your password must contain at least one digit')
        if password == password.lower():
            raise NoUpperLettersInPassword(' ! Error, your password must contain at least one capital letter')
        if not re.sub(r'\w', '', password):
            raise NoSpecificLettersInPassword('! Error, your password must contain at least one specific letter')
    except IncorrectLengthUserPassword as error:
        verification_animation()
        print(error)
        exit()
    except NoDigitInPassword as error:
        verification_animation()
        print(error)
        exit()
    except NoUpperLettersInPassword as error:
        verification_animation()
        print(error)
        exit()
    except NoSpecificLettersInPassword as error:
        verification_animation()
        print(error)
        exit()

    verification_animation()
    print(' ✅ Good password')
    return password


def check_incasator_number_banknotes_pick_up(prompt: str, number_banknotes: int) -> int | bool:
    """Checks the input data about the banknote from the collector.
       It also restricts the possibility of withdrawing more banknotes than there are in the ATM."""

    while True:
        try:
            number_banknotes_withdrawal = input(prompt)
            if not number_banknotes_withdrawal:
                return False
            if int(number_banknotes_withdrawal) > number_banknotes:
                raise IncorrectNumberBanknotesWithdrawal(' ! Error, banknotes in atm less than your request.\n')
            return int(number_banknotes_withdrawal)
        except IncorrectNumberBanknotesWithdrawal as error:
            sleep(1)
            print(error)
        except ValueError:
            sleep(1)
            print(' ! Error, enter please a number\n')


def check_input_incasator_denomination_banknote(prompt: str) -> int | None:
    """Verification of incoming data from the cash collector for compliance with the banknote denomination"""

    while True:
        try:
            number = input(prompt)
            if not number:
                return False
            if number not in ('10', '20', '50', '100', '200', '500', '1000'):
                raise IncorrectDenominationBanknote(' ! Error, incorrect denomination of the banknote, try again\n')
            return int(number)
        except IncorrectDenominationBanknote as error:
            sleep(1)
            print(error)
        except ValueError:
            sleep(1)
            print(' ! Error, enter please a number\n')
