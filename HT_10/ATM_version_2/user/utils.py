import sqlite3
import os
from time import sleep
from HT_10.ATM_version_2.main import verification_animation
from HT_10.ATM_version_2.incasator.utils import incasator_menu


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
            incasator_menu(username)
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
