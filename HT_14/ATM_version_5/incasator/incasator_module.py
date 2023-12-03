import sqlite3
import os
from prettytable import PrettyTable
from HT_14.ATM_version_5.main import sub_menu
from time import sleep
from HT_14.ATM_version_5.atm.atm_module import ATM
from HT_14.ATM_version_5.main import start


class IncorrectDenominationBanknote(Exception):
    pass


class IncorrectNumberBanknotesWithdrawal(Exception):
    pass


class Incasator:

    @staticmethod
    def information_about_users(username: str) -> None:
        """"""

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT login, Operation, Date
                              FROM users_transactions
                              WHERE Operation == ?""",
                           ('Registration',))

            table = PrettyTable()
            table.field_names = ['User login', 'Operation', 'Date']
            result_users_transactions = cursor.fetchall()

            for line in result_users_transactions:
                table.add_row(line)

            print(table)

    @staticmethod
    def user_transactions(username: str) -> None:
        """"""

        print('\n____________________\n'
              '1. Transactions of all users\n'
              '2. Search transactions by user\n'
              '\n'
              '0. Back to main menu\n'
              '▼')

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()

            while True:

                match input('Your choice: '):
                    case '1':
                        cursor.execute("""SELECT login, Operation, Amount, Date
                                                FROM users_transactions
                                                WHERE Operation != ?""",
                                       ('Registration',))

                        table = PrettyTable()
                        table.field_names = ['User login', 'Operation', 'Amount', 'Date']
                        result_users_transactions = cursor.fetchall()

                        for line in result_users_transactions:
                            table.add_row(line)

                        sleep(1)
                        print(table)
                        sub_menu(username)

                    case '2':
                        while True:
                            search_user = input('Enter username for search: ')

                            cursor.execute("""SELECT login, Operation, Amount, Date
                                                   FROM users_transactions
                                                   WHERE Operation != ? and login = ?""",
                                           ('Registration', search_user))

                            table = PrettyTable()
                            table.field_names = ['User login', 'Operation', 'Amount', 'Date']
                            result_users_transactions = cursor.fetchall()

                            if len(result_users_transactions) > 0:
                                for line in result_users_transactions:
                                    table.add_row(line)

                                sleep(1)
                                print(table)
                                sub_menu(username)
                            sleep(1)
                            print(' ! Error, user with this name was not found.\n')
                            sub_menu(username)
                    case '0':
                        sleep(1)
                        Incasator.incasator_menu(username)
                    case '':
                        print('❎ Cancel operation')
                        sleep(1)
                        sub_menu(username)
                    case _:
                        print(' ! Error number, try again\n')
                        sleep(1)
                        # sub_menu(username)

    @staticmethod
    def incasator_menu(username: str) -> None:
        """Incasator_menu menu for using the program"""

        while True:
            print(f'\n____________________\n'
                  f'Incasator menu:\n'
                  f'𝟏. Information about users\n'
                  f'2. User transactions\n'
                  f'3. Balance ATM\n'
                  f'4. Change balance ATM\n'
                  f'5. ATM balance transactions\n'
                  f'\n'
                  f'𝟎. Exit\n'
                  f'𝟗. Log out\n'
                  f'▼')

            match input('Your choice: '):
                case '1':
                    sleep(1)
                    Incasator.information_about_users(username)
                    sub_menu(username)
                case '2':
                    sleep(1)
                    Incasator.user_transactions(username)

                    sub_menu(username)
                case '3':
                    sleep(1)
                    ATM.balance_atm()
                    sub_menu(username)
                case '4':
                    sleep(1)
                    ATM.change_balance_atm(username)
                    sub_menu(username)
                case '5':
                    sleep(1)
                    ATM.show_atm_balance_transactions()
                    sub_menu(username)
                case '0':
                    print('\n♥ Bye ♥')
                    exit()
                case '9':
                    sleep(1)
                    print('♥ Bye ♥\n')
                    sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    start()
                case _:
                    print(' ! Error number, try again')
                    sleep(1)

    @staticmethod
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

    @staticmethod
    def check_input_denomination_banknote(prompt: str) -> int | None:
        """Checking user input values for type matching"""

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
