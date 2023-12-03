import sqlite3
import requests
from time import sleep
from datetime import datetime
from prettytable import PrettyTable
from HT_14.ATM_version_5.system.system_module import check_file, check_input_user_data
from HT_14.ATM_version_5.main import deposit_time_animation
from HT_14.ATM_version_5.system.system_module import check_username_for_transfer
from HT_14.ATM_version_5.main import sub_menu


class ATM:
    @staticmethod
    def withdraw_balance(amount_funds: int, username) -> bool:
        full_path = check_file()

        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            query = sorted(cursor.execute("""SELECT banknote, number_of_banknotes
                                      FROM atm_balance
                                      """
                                          ).fetchall(), reverse=True)
        banknote_counts = {}
        original_money_funds = amount_funds
        withdraw_banknotes1 = []

        for banknote, number_banknotes in query:
            if not number_banknotes:
                continue
            number = amount_funds // banknote
            if number > number_banknotes:
                amount_funds = amount_funds - (number_banknotes * banknote)
                banknote_counts.setdefault(banknote, 0)
                withdraw_banknotes1.extend([banknote] * number)
                continue

            if not number:
                continue

            banknote_counts.setdefault(banknote, number_banknotes - number)
            withdraw_banknotes1.extend([banknote] * number)
            amount_funds = amount_funds % banknote

            if amount_funds == 0:
                d = {banknote: withdraw_banknotes1.count(banknote) for banknote in withdraw_banknotes1}

                for banknote1, number_banknotes1 in banknote_counts.items():
                    cursor.execute(
                        """UPDATE atm_balance 
                        SET number_of_banknotes = ? , sum_of_all_banknotes = ?
                        WHERE banknote= ?""",
                        (number_banknotes1, number_banknotes1 * banknote1, banknote1))
                    db.commit()
                print('\nYour bills:')
                for banknote1, number_banknotes1 in d.items():
                    print(f'{banknote1} x {number_banknotes1}')
                print()
                return True

        banknotes = [group[0] for group in query for _ in range(group[1])]

        banknote_and_number = {0: 0}

        for i in range(1, len(banknotes)+1):
            value = banknotes[i-1]
            new_banknote_counts = {}
            for suma in banknote_and_number.keys():
                new_sum = suma + value
                if new_sum > original_money_funds:
                    continue
                elif new_sum not in banknote_and_number.keys():
                    new_banknote_counts[new_sum] = value
            banknote_and_number = banknote_and_number | new_banknote_counts
            if original_money_funds in banknote_and_number.keys():
                break

        withdraw_banknotes = []
        if original_money_funds not in banknote_and_number.keys():
            sleep(1)
            print(" ! Error, there are no banknotes to issue the specified amount")
            sleep(1)
            return False
        else:
            value = original_money_funds
            while value > 0:
                withdraw_banknotes.append(banknote_and_number[value])
                value -= banknote_and_number[value]

        banknote_upload = dict(query)
        banknote_out = {i: withdraw_banknotes.count(i) for i in withdraw_banknotes}
        for key, value in banknote_out.items():
            banknote_upload[key] -= value

        for banknote, number_of_banknotes in banknote_upload.items():
            with sqlite3.connect(full_path) as db:
                cursor = db.cursor()
                cursor.execute(
                    """UPDATE atm_balance 
                    SET number_of_banknotes = ? , sum_of_all_banknotes = ?
                    WHERE banknote= ?""",
                    (number_of_banknotes, number_of_banknotes * banknote, banknote))
                db.commit()
        d = {banknote: withdraw_banknotes.count(banknote) for banknote in withdraw_banknotes}

        print('\nYour bills:')
        for banknote, number_banknotes in d.items():
            print(f'{banknote} x {number_banknotes}')
        print()
        return True

    @staticmethod
    def deposit_money(username: str):
        """"""

        from HT_14.ATM_version_5.user.user_module import User
        from HT_14.ATM_version_5.system.system_module import add_transactions

        print(f'-------------------\n'
              f'Welcome.\n'
              f'You can put money on a deposit with us at different interest rates.\n'
              'The interest rate will depend on the number of years for which you put the money, namely:\n'
              ' - 1 year  -> 10%.\n'
              ' - 2 years -> 12%.\n'
              ' - 3 years -> 15%.\n'
              ' - 4 years -> 17%.\n'
              ' - 5 years -> 20%\n')

        percents = {1: 10, 2: 12, 3: 15, 4: 17, 5: 20}

        sleep(1)
        minimum_multiplicity_of_withdrawal, *_ = min(ATM.balance_atm('withdrawal'), key=lambda banknote: banknote[0])
        amount_balance = User.show_balance(username)
        print(f'-------------------\n'
              f'Minimum multiplicity of deposit: {minimum_multiplicity_of_withdrawal}$\n'
              f'Minimum value for deposit: 100$')

        while True:
            start_amount = int(check_input_user_data('How much money do you want to deposit? '
                                                     '(or press "Enter" to cancel): '))
            if not start_amount:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)
            if start_amount < 0:
                sleep(1)
                print(' ! Error, the amount cannot be negative.\n')
                continue
            if start_amount % minimum_multiplicity_of_withdrawal:
                sleep(1)
                print('! Error, amount does not meet the minimum multiplicity, try again\n')
                sleep(1)
                continue
            if start_amount > amount_balance:
                sleep(1)
                print(f'\nError, the deposit amount is lower than the amount available on the account.'
                      f'\n!Your balance is {amount_balance}$\n'
                      f'Enter a smaller amount\n')
                sleep(1)
                continue
            if start_amount < 100:
                sleep(1)
                print(' ! Error, deposit amount is below the minimum.\n')
                sleep(1)
                continue
            if start_amount % minimum_multiplicity_of_withdrawal:
                sleep(1)
                print('! Error, amount does not meet the minimum multiplicity, try again\n')
                sleep(1)
                continue
            break

        while True:
            count_years = int(check_input_user_data('For how many years do you want to deposit money? '
                                                    '(or press "Enter" to cancel): '))
            if not count_years:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)
            if count_years not in range(1, 6):
                sleep(1)
                print(' ! Error, incorrect count years. Try again\n')
                sleep(1)
                continue
            break

        percent_money = 0

        for i in range(count_years):
            percent_money += start_amount * (percents[count_years] / 100)

        deposit_time_animation(count_years)
        sleep(1)

        print(f'\n\nYour deposit time has come to an end.\n'
              f'You deposited {start_amount}$ money.\n'
              f'You received {round(percent_money, 2)}$ in interest for {count_years} year/years.\n'
              f'In total, we will back to your account with {int(start_amount + (percent_money // 10) * 10)}$.')

        if (start_amount + percent_money) % 10:
            print(
                f'\nThe rest in the amount of {round(percent_money - (percent_money // 10) * 10, 2)}$ is given to you\n'
                f'\n'
                f'Thank you for choosing us. ♥ ')
            percent_money = (percent_money // 10) * 10

        sleep(3)

        add_transactions(username, int(percent_money), amount_balance, 3)
        User.change_balance(username, percent_money, 'deposit')
        sleep(1)
        print('✅ Complete operation')
        sub_menu(username)

    @staticmethod
    def transfer_money(username):

        from HT_14.ATM_version_5.system.system_module import add_transactions
        from HT_14.ATM_version_5.user.user_module import User

        transfer_balance = User.show_balance(username)
        if not transfer_balance:
            print(f'\nThe transfer operation is not available because your balance is {transfer_balance}$.\n'
                  f'Replenishment money first.')
            sub_menu(username)

        minimum_multiplicity_of_withdrawal, *_ = min(ATM.balance_atm('withdrawal'), key=lambda banknote: banknote[0])

        print(f'-------------------'
              f'\nNow in your balance: {transfer_balance}$\n'
              f'Minimum multiplicity of transfer: {minimum_multiplicity_of_withdrawal}$')
        while True:
            receiver_username = input('Enter the name of the recipient of the transfer (or press "Enter" to cancel): ')
            if not receiver_username:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)

            if not check_username_for_transfer(receiver_username):
                continue
            break
        received_balance = User.show_balance(receiver_username)
        total_amount_money_in_atm = sum(number[0] * number[1] for number in ATM.balance_atm('sum'))

        while True:
            amount_transfer = int(check_input_user_data('How much money you want to transfer '
                                                        '(or press "Enter" to cancel)?: '))
            if not amount_transfer:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)
            if amount_transfer < 0:
                sleep(1)
                print(' ! Error, the amount cannot be negative.\n')
                continue
            if amount_transfer % minimum_multiplicity_of_withdrawal:
                sleep(1)
                print('! Error, amount does not meet the minimum multiplicity, try again\n')
                sleep(1)
                continue
            if amount_transfer > total_amount_money_in_atm:
                sleep(1)
                print('! Error, amount of the transfer is more than the money in ATM, please enter a smaller amount\n')
                sleep(1)
                continue

            if amount_transfer > transfer_balance:
                sleep(1)
                print(f'\nError, the transfer amount is higher than the amount available on the account.'
                      f'\n!Your balance is {transfer_balance}$\n'
                      f'Enter a smaller amount\n')
                sleep(1)
                continue
            break

        add_transactions(username, -amount_transfer, transfer_balance, 4)
        add_transactions(receiver_username, amount_transfer, received_balance, 5)

        User.change_balance(username, -abs(amount_transfer), 'transfer')
        User.change_balance(receiver_username, amount_transfer, 'transfer')
        sleep(1)
        print('✅ Complete operation')
        sub_menu(username)

    @staticmethod
    def balance_atm(operation=None) -> list | None:
        """Allows you to get the ATM balance in the form of a table
        with the values of the banknote name and their quantity"""

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
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

        from HT_14.ATM_version_5.incasator.incasator_module import Incasator
        from HT_14.ATM_version_5.system.system_module import check_file, check_input_user_data

        full_path = check_file()
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
                choice = int(check_input_user_data('Your choice: '))
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

                banknote = Incasator.check_input_denomination_banknote('Enter the denomination of the banknote '
                                                             'you want to change (or press "Enter" to cancel): ')
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
                        number_of_banknotes = check_input_user_data('Enter the number of banknotes you want to add '
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
                        number_of_banknotes = Incasator.check_incasator_number_banknotes_pick_up('Enter the '
                                                                                                 'number of banknotes '
                                                                                       'you want to pick up '
                                                                                       '(or press "Enter" to cancel): ',
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
            ATM.add_atm_balance_transactions(username, banknote, number_of_banknotes_before_upd,
                                             update_number_of_banknotes)

    @staticmethod
    def add_atm_balance_transactions(username: str, banknote: int, before_update: int, after_update: int) -> None:
        """Adds a transaction to the corresponding table to change the atm balance"""

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
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

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
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

            print('\n                                     ATM BALANCE TRANSACTIONS                                 ')
            print(table)

            return

    @staticmethod
    def get_current_exchange_rate(username: str):
        """"""

        url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5'

        datas = requests.get(url).json()
        print(f'\nToday: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

        for data in datas:
            print(f'{data["ccy"]}:\n'
                  f'Buy: {data["buy"]}\n'
                  f'Sale: {data["sale"]}\n')
        sleep(1)
        sub_menu(username)
