import sqlite3
from prettytable import PrettyTable
from time import sleep
from HT_11.ATM_version_3.main import sub_menu
from datetime import datetime


class Atm:
    @staticmethod
    def balance_atm(operation=None) -> list | None:
        """Allows you to get the ATM balance in the form of a table
        with the values of the banknote name and their quantity"""

        from HT_11.ATM_version_3.user.user_module import User

        full_path = User.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()

            if operation in ('replenishment', 'withdrawal'):
                cursor.execute("""SELECT banknote
                                  FROM atm_balance
                                  WHERE number_of_banknotes != '0'
                              """)
                result_users_transactions = cursor.fetchall()
                return result_users_transactions

            cursor.execute("""SELECT banknote, number_of_banknotes
                              FROM atm_balance""")
            result_users_transactions = cursor.fetchall()

            if operation == 'sum':
                return result_users_transactions

            total_amount_money_in_atm = sum(number[0] * number[1] for number in result_users_transactions)

            table = PrettyTable()
            table.field_names = ['Banknote', 'Amount']

            for line in result_users_transactions:
                table.add_row(line)

            print('\n* ATM BALANCE SHEET *')
            print(table)
            print(f'Total balance - {total_amount_money_in_atm}$')

    @staticmethod
    def change_balance_atm(username: str) -> None:
        """Allows you to change the ATM balance by selecting the desired banknote.
        Allows you to add banknotes and withdraw them."""

        from HT_11.ATM_version_3.incasator.incasator_module import Incasator
        from HT_11.ATM_version_3.user.user_module import User

        full_path = User.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()

            print('----------------'
                  '\nWhat kind of operations do you want to make?\n'
                  '1. Add banknotes\n'
                  '2. Pick up banknotes\n'
                  '\n'
                  '0. Back\n'
                  '▼')

            while True:
                choice = int(User.check_input_user_data('Your choice: '))
                if choice not in (1, 2, 0):
                    sleep(1)
                    print(' ! Error, need number (1, 2 or 0). Try again.\n')
                    continue
                if not choice:
                    sleep(1)
                    Incasator.incasator_menu(username)

                sleep(1)
                print('!Attention!\n'
                      'Banknote denominations that can be used to add: 𝟏𝟎, 𝟐𝟎, 𝟓𝟎, 𝟐𝟎𝟎, 2𝟎𝟎, 𝟓𝟎𝟎, 𝟏𝟎𝟎𝟎')

                banknote = Incasator.check_input_incasator_denomination_banknote('Enter the denomination of the '
                                                                                 'banknote you want to change '
                                                                                 '(or press "Enter" to cancel): ')
                if not banknote:
                    sleep(1)
                    print('❎ Cancel operation')
                    sub_menu(username)

                cursor.execute("""SELECT number_of_banknotes
                                  FROM atm_balance
                                  WHERE banknote = ?""",
                               (banknote,))

                number_of_banknotes_before_upd, *_ = cursor.fetchone()

                sleep(1)
                print(f'Currently {number_of_banknotes_before_upd} banknotes of this denomination in the ATM')

                if choice == 1:
                    while True:
                        number_of_banknotes = User.check_input_user_data(
                            'Enter the number of banknotes you want to add '
                            '(or press "Enter" to cancel): ')
                        if not number_of_banknotes:
                            sleep(1)
                            print('❎ Cancel operation')
                            sub_menu(username)
                        if number_of_banknotes < 0:
                            sleep(1)
                            print(' ! Error, the number cannot be negative.\n')
                            continue
                        break
                    update_number_of_banknotes = number_of_banknotes_before_upd + number_of_banknotes

                    cursor.execute("""UPDATE atm_balance
                                      SET number_of_banknotes = ?
                                      WHERE banknote = ?""",
                                   (update_number_of_banknotes, banknote))
                    db.commit()
                    break

                elif choice == 2:
                    if number_of_banknotes_before_upd == 0:
                        print('It is impossible to perform a transaction for this banknote '
                              'because it is not available in the ATM')
                        sleep(1)
                        sub_menu(username)
                    while True:
                        number_of_banknotes = Incasator.check_incasator_number_banknotes_pick_up(
                            'Enter the number of banknotes you want to pickup (or press "Enter" to cancel): ',
                            number_of_banknotes_before_upd)
                        if not number_of_banknotes:
                            sleep(1)
                            print('❎ Cancel operation')
                            sub_menu(username)
                        if number_of_banknotes < 0:
                            sleep(1)
                            print(' ! Error, the number cannot be negative.\n')
                            continue
                        break
                    update_number_of_banknotes = number_of_banknotes_before_upd - number_of_banknotes
                    cursor.execute("""UPDATE atm_balance
                                      SET number_of_banknotes = ?
                                      WHERE banknote = ?""",
                                   (update_number_of_banknotes, banknote))
                    db.commit()
                    break

                elif choice == 0:
                    Incasator.incasator_menu(username)

            update_sum_of_banknotes = update_number_of_banknotes * banknote
            cursor.execute("""UPDATE atm_balance
                              SET sum_of_all_banknotes  = ?
                              WHERE banknote = ?""",
                           (update_sum_of_banknotes, banknote))

            db.commit()
            sleep(1)
            print('✅ Complete operation')
            Atm.add_atm_balance_transactions(username, banknote, number_of_banknotes_before_upd,
                                             update_number_of_banknotes)

    @staticmethod
    def add_atm_balance_transactions(username: str, banknote: int, before_update: int, after_update: int) -> None:
        """Adds a transaction to the corresponding table to change the atm balance"""

        from HT_11.ATM_version_3.user.user_module import User

        full_path = User.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO atm_balance_transactions
                              ('name', 'banknote', 'Operation', 'was_number_of_banknotes',
                              'became_number_of_banknotes', 'date')
                              VALUES (?, ?, ?, ?, ?, ?)""",
                           (username, banknote,
                            f'Add banknotes' if before_update < after_update else 'Pick up banknotes',
                            before_update, after_update, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()
            return

    @staticmethod
    def show_atm_balance_transactions() -> None:
        """Displays the data in the form of a table showing all operations
           performed by the cash collector with the atm balance"""

        from HT_11.ATM_version_3.user.user_module import User

        full_path = User.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT name, banknote, Operation, was_number_of_banknotes, became_number_of_banknotes, date
                              FROM atm_balance_transactions""")

            table = PrettyTable()
            table.field_names = ['Name', 'Banknote', 'Operation', 'Was number of banknotes',
                                 'Became number of banknotes', 'Date']

            result_users_transactions = cursor.fetchall()

            for line in result_users_transactions:
                table.add_row(line)

            print(table)

            return
