import sqlite3
import re
from time import sleep
from datetime import datetime
from HT_10.ATM_version_2.user.utils import check_file
from HT_10.ATM_version_2.main import verification_animation


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
    """Adding a new user to a database"""

    print('\n**************************'
          '\nThe rule for registration:\n'
          ' - the username should not contain spaces and the length should be from 3 to 15 characters\n'
          ' - password must be at least 8 characters long\n'
          ' - the password must contain at least one digit, a capital letter and a special character\n'
          'P.S. If you change your mind and want to exit, press Enter\n')

    print('• Registration form •')

    username = validation_username(input('Create your username: '))
    password = validation_password(input('Create your password: '))

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


def validation_username(username) -> str:
    """Checking the username for compliance with the requirements"""

    try:
        if not username:
            print('❎ Cancel registration\n'
                  '\n♥ Bye ♥')
            exit()
        if not 3 <= len(username) <= 15:
            raise IncorrectLengthUsername(' ! Error, username is not the right length (need length between 3 and 15)')
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
            raise IncorrectLengthUserPassword(' ! Error, your password is too short (must be more than 8 characters)')
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
