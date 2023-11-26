""" 3. Програма-банкомат.
   Використовуючи функції створити програму з наступним функціоналом:
      - підтримка 3-4 користувачів, які валідуються парою ім'я/пароль (файл <users.CSV>);
      - кожен з користувачів має свій поточний баланс (файл <{username}_balance.TXT>) та
        історію транзакцій (файл <{username_transactions.JSON>);
      - є можливість як вносити гроші, так і знімати їх. Обов'язкова перевірка введених
        даних (введено цифри; знімається не більше, ніж є на рахунку і т.д.).
   Особливості реалізації:
      - файл з балансом - оновлюється кожен раз при зміні балансу
        (містить просто цифру з балансом);
      - файл - транзакціями - кожна транзакція у вигляді JSON рядка
        додається в кінець файла;
      - файл з користувачами: тільки читається. Але якщо захочете
        реалізувати функціонал додавання нового користувача - не стримуйте себе :)
   Особливості функціонала:
      - за кожен функціонал відповідає окрема функція;
      - основна функція - <start()> - буде в собі містити весь workflow банкомата:
      - на початку роботи - логін користувача (програма запитує ім'я/пароль).
        Якщо вони неправильні - вивести повідомлення про це і закінчити роботу
        (хочете - зробіть 3 спроби, а потім вже закінчити роботу - все на ентузіазмі :))
      - потім - елементарне меню типн:
        Введіть дію:
           1. Подивитись баланс
           2. Поповнити баланс
           3. Вихід
      - далі - фантазія і креатив, можете розширювати функціонал, але основне завдання
        має бути повністю реалізоване :)
    P.S. Увага! Файли мають бути саме вказаних форматів (csv, txt, json відповідно)
    P.S.S. Добре продумайте структуру програми та функцій """

import os
import csv
from time import sleep
from datetime import datetime
import json
from prettytable import PrettyTable
import re


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


def menu(username) -> None:
    """User menu for using the program"""

    while True:
        print(f'\n____________________\n'
              f'Menu:\n'
              f'𝟏. Withdrawal\n'
              f'𝟐. Deposit money\n'
              f'𝟑. Show balance\n'
              f'𝟒. Transactions\n'
              f'𝟎. Exit\n'              
              f'▼')

        match input('Your choice: '):
            case '1':
                sleep(1)
                withdrawal(username)
            case '2':
                sleep(1)
                deposit_money(username)
            case '3':
                sleep(1)
                print(f'--------------\n'
                      f'Money on your balance: {show_balance(username)}$')
                sub_menu(username)
            case '4':
                sleep(1)
                show_transactions(username)
                sub_menu(username)
            case '0':
                print('\n♥ Bye ♥')
                exit()
            case _:
                print(' ! Error number, try again')
                sleep(1)


def sub_menu(username) -> None:
    """Sub menu for the user"""

    print('▼\n'
          '1. Back to main menu\n'
          '0. Exit')

    match input('Your choice: '):
        case '1':
            sleep(1)
            menu(username)
        case '0':
            print('\n♥ Bye ♥')
            exit()
        case _:
            print(' ! Error number, try again\n')
            sleep(1)
            sub_menu(username)


def verification_animation() -> None:
    """Displays an animation of waiting for data verification"""

    print('Check', end='', flush=True)
    for _ in range(3):
        sleep(1)
        print('.', end='', flush=True)
    return


def add_new_users() -> bool:
    """Adding a new user to a file"""

    print('\n**************************'
          '\nThe rule for registration:\n'
          ' - the username should not contain spaces and the length should be from 3 to 15 characters\n'
          ' - password must be at least 8 characters long\n'
          ' - the password must contain at least one digit, a capital letter and a special character\n'
          'P.S. If you change your mind and want to exit, press Enter\n')

    print('• Registration form •')

    username = validation_username(input('Create your username: '))
    password = validation_password(input('Create your password: '))

    with open(os.path.join(os.getcwd(), 'users.csv'), 'a', newline='', encoding='utf-8') as file:

        if all(isinstance(elem, str) for elem in (username, password)):
            writer = csv.writer(file)
            writer.writerow([username, password])
            print('Registration complete. Use your data for authorization')
            sleep(1)

            create_new_balance_file_for_new_users(username)
            create_new_transactions_file_for_new_users(username)
            return True

        exit()


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


def check_username_exists(username) -> bool:
    """Checking the username for uniqueness"""

    full_path = check_file(os.path.join(os.getcwd(), 'users.csv'))

    with open(full_path, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if username not in row:
                continue
            print(' ❗ A user with this name already exists. Try again')
            exit()

        return True


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


def create_new_balance_file_for_new_users(username: str) -> bool:
    """Create a new directory with a username with a balance sheet file"""

    dir_files = os.path.join(os.getcwd(), 'users', username)
    os.makedirs(os.path.join(dir_files))
    with open(os.path.join(dir_files, f'{username}_balance.txt'), 'w', encoding='utf-8') as file:
        file.write('0')
        return True


def show_balance(username: str) -> str:
    """View the user's balance and overwrite the balance after the selected transaction"""

    full_path = check_file(os.path.join(os.getcwd(), 'users', username, f'{username}_balance.txt'))
    with open(full_path, encoding='utf-8') as file_read:
        file_read = file_read.read()
        return file_read


def change_balance(username: str, money_request=None) -> None | bool:
    """Changes the user's balance file after each operation"""

    amount_balance = float(show_balance(username))

    if amount_balance + money_request > 0:
        with open(os.path.join(os.getcwd(), 'users', username, f'{username}_balance.txt'), 'w') as file_write:
            file_write.write(str(amount_balance + money_request))
            print('✅ Complete operation')
            return True

    sleep(1)
    if amount_balance:
        print(f'\nError, the withdrawal amount is higher than the amount available on the account.'
              f'\n!Your balance is {amount_balance}$\n'
              f'Enter a smaller amount\n')
        sleep(1)
        sub_menu(username)
    else:
        print(f'\nError, the withdrawal amount is higher than the amount available on the account.'
              f'\n!Your balance is {amount_balance}$\n'
              f'Deposit money first.\n')
        sleep(1)
        sub_menu(username)


def withdrawal(username: str) -> None:
    """Withdrawing money from the user's balance"""

    money_withdrawal = check_input_user_data('How much money you want to withdrawal?: ')
    if change_balance(username, -abs(money_withdrawal)):
        add_transactions(username, -abs(money_withdrawal))
        sleep(1)
        sub_menu(username)


def deposit_money(username: str) -> None:
    """Adding money to the user's balance"""

    money_deposit = check_input_user_data('How much money you want to deposit?: ')
    change_balance(username, abs(money_deposit))
    add_transactions(username, abs(money_deposit))
    sleep(1)
    sub_menu(username)


def create_new_transactions_file_for_new_users(username: str) -> bool:
    """Create a new transaction file for a new user"""

    dir_files = os.path.join(os.getcwd(), 'users', username)
    with open(os.path.join(dir_files, f'{username}_transactions.json'), 'w', encoding='utf-8') as file:
        first_data = \
            [{
                "Operation": "Registration",
                "Amount": 0,
                "Date": f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }]
        json.dump(first_data, file, indent=3)
        return True


def show_transactions(username: str, option=1) -> dict:
    """Viewing user transactions from a file as a formatted table"""

    full_path = check_file(os.path.join(os.getcwd(), 'users', username, f'{username}_transactions.json'))
    with open(full_path, encoding='utf-8') as file:
        data_operations = json.load(file)
        if option:
            table = PrettyTable()
            table.field_names = data_operations[0].keys()

            for i in data_operations:
                table.add_row(i.values())

            print('\n***             TRANSACTIONS                 ***')
            print(table)

        return data_operations


def add_transactions(username: str, funds: float, option=0) -> None:
    """Adding a user transaction to the end of a file"""

    total_transaction_operation = show_transactions(username, option)

    if funds:
        new_transactions = \
            {
                "Operation": f'{"Withdrawal" if funds < 0 else "Deposit"}',
                "Amount": abs(funds),
                "Date": f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            }
        total_transaction_operation.append(new_transactions)

    with open(os.path.join(os.getcwd(), 'users', username, f'{username}_transactions.json'), 'w') as file:
        json.dump(total_transaction_operation, file, indent=3)


def check_login_data() -> str | bool:
    """Check user login data for presence in the file"""

    full_path = check_file(os.path.join(os.getcwd(), 'users.csv'))
    username = input('Enter your username: ')
    user_password = input('Enter your password: ')

    with open(full_path, encoding='utf-8') as file_users:
        reader = csv.reader(file_users)
        next(reader)
        for row in reader:
            if [username, user_password] == row:
                verification_animation()
                print(' ✅ Login successful')

                sleep(1)
                return username

        verification_animation()
        print(' ! Error, username or password incorrect.')
        return False


def check_input_user_data(prompt: str) -> float:
    """Checking user input values for type matching"""

    while True:
        try:
            number = float(input(prompt))
            return number
        except ValueError:
            print(' ! Error, enter please a number\n')


def check_file(path: str) -> str:
    """Checking a file for existence on a given path"""

    try:
        with open(path, encoding='utf-8') as file:
            return path
    except FileNotFoundError as error:
        print(error)
        exit()


def start() -> None:
    """Main controller"""

    print('▼\n'
          'Here are the available features of this ATM.\n'
          ' • withdraw money from your account\n'
          ' • deposit money to your account\n'
          ' • view your account transactions\n'
          'If you are not our client, you can register '
          '(you will need to come up with a username and a "good" password).\n'
          'After that, you will also have access to the full functionality of the ATM.')

    while True:
        print('\n--------------------\n'
              'Choose what you want\n'
              '①. Registration\n'
              '②. Log in\n'
              '⓪. Exit\n'
              '  ▼')

        match input('Input operation number to continue: '):
            case '1':
                sleep(1)
                add_new_users()
            case '2':
                for i in range(3, 0, -1):
                    sleep(1)
                    print(f'\n • Authorization •')
                    result_check_users_name = check_login_data()

                    if result_check_users_name:
                        menu(result_check_users_name)

                    if i > 1:
                        print(f'You have {i - 1} more tries')
                        continue

                sleep(1)
                print(f'\nWe are sorry, but you have entered your data incorrectly 3 times and your account has '
                      'been temporarily blocked.\nTo resolve the issue, please email us at fildaiko@gmail.com')
                exit()
            case '0':
                sleep(1)
                print('\n♥ Bye ♥')
                exit()
            case _:
                print(' ! Error. Please, enter a correct number operation (1, 2 or 3). Try again')
                sleep(1)


if __name__ == '__main__':
    start()
