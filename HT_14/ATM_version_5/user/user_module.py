import sqlite3
from time import sleep
from HT_14.ATM_version_5.atm.atm_module import ATM
from HT_14.ATM_version_5.system.system_module import add_transactions
from HT_14.ATM_version_5.main import sub_menu


class User:
    @staticmethod
    def show_balance(username: str) -> int:
        """View the user's balance and overwrite the balance after the selected transaction"""

        from HT_14.ATM_version_5.system.system_module import check_file

        full_path = check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""SELECT balance
                              FROM users_balance
                              WHERE login == ?""",
                           (username,))

            result, *_ = cursor.fetchone()
            return result

    @staticmethod
    def change_balance(username: str, money_request=None, operation=None) -> None | bool:
        """Changes the user's balance file after each operation"""

        from HT_14.ATM_version_5.system.system_module import check_file

        amount_balance = User.show_balance(username)
        full_path = check_file()
        if amount_balance + money_request >= 0:
            with sqlite3.connect(full_path) as db:
                cursor = db.cursor()
                cursor.execute("""UPDATE users_balance
                                  SET balance = ?
                                  WHERE login == ?""",
                               (amount_balance + money_request, username))

                if not operation:
                    sleep(1)
                    print('✅ Complete operation')
                    return True

    @staticmethod
    def withdrawal(username: str) -> None:
        """Withdrawing money from the user's balance"""

        from HT_14.ATM_version_5.system.system_module import check_input_user_data

        total_amount_money_in_atm = sum(number[0] * number[1] for number in ATM.balance_atm('sum'))
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

        minimum_multiplicity_of_withdrawal, *_ = min(ATM.balance_atm('withdrawal'), key=lambda banknote: banknote[0])
        sleep(1)
        print(f'Now in your balance: {amount_balance}$')
        # print(f'Now in your balance: {amount_balance}$\n'
        #       f'Minimum multiplicity of withdrawal: {minimum_multiplicity_of_withdrawal}$')

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
            # if money_withdrawal % minimum_multiplicity_of_withdrawal:
            #     sleep(1)
            #     print('! Error, amount does not meet the minimum multiplicity, try again\n')
            #     sleep(1)
            #     continue

            if money_withdrawal > total_amount_money_in_atm:
                sleep(1)
                print('! Error, amount of the withdrawal is more than the money in ATM, please enter a smaller amount\n')
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

        if ATM.withdraw_balance(money_withdrawal, username) and User.change_balance(username, -money_withdrawal):
            add_transactions(username, -money_withdrawal, amount_balance, 1)
            sub_menu(username)
        sub_menu(username)

    @staticmethod
    def replenishment_money(username: str) -> None:
        """Adding money to the user's balance"""

        from HT_14.ATM_version_5.system.system_module import check_input_user_data

        amount_balance = User.show_balance(username)

        minimum_multiplicity_of_replenishment, *_ = min(ATM.balance_atm('replenishment'), key=lambda banknote: banknote[0])
        sleep(1)
        print(f'Minimum multiplicity of replenishment: {minimum_multiplicity_of_replenishment}$')

        while True:
            money_replenishment = float(check_input_user_data('How much money you want to replenishment '
                                                              '(or press "Enter" to cancel)?: '))
            if not money_replenishment:
                sleep(1)
                print('❎ Cancel operation')
                sub_menu(username)
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

            User.change_balance(username, abs(final_money_replenishment))
            add_transactions(username, int(abs(final_money_replenishment)), amount_balance, 2)
            sub_menu(username)
