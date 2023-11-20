import sqlite3
from time import sleep
from HT_10.ATM_version_2.user.utils import check_file, check_input_user_data
# from HT_10.ATM_version_2.atm.atm import change_number_banknotes_when_user_withdraws
from HT_10.ATM_version_2.atm.balance import balance_atm
from HT_10.ATM_version_2.user.transactions import add_transactions
from HT_10.ATM_version_2.main import sub_menu


def show_balance(username: str) -> int:
    """View the user's balance"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()
        cursor.execute("""SELECT balance
                          FROM users_balance
                          WHERE login == ?""",
                       (username,))

        result, *_ = cursor.fetchone()
        return result


def change_balance(username: str, money_request=None) -> None | bool:
    """Updates the user's balance in the database after a withdrawal or replenishment operation"""

    amount_balance = show_balance(username)
    full_path = check_file()
    if amount_balance + money_request >= 0:
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""UPDATE users_balance
                              SET balance = ?
                              WHERE login == ?""",
                           (amount_balance + money_request, username))

            print('✅ Complete operation')
            return True
    sleep(1)
    sub_menu(username)


def withdrawal(username: str) -> None:
    """It allows withdrawing funds from the user's balance,
       as well as handles options when the user has no money on the balance or the ATM itself has no money"""

    total_amount_money_in_atm = sum(number[0] * number[1] for number in balance_atm('sum'))
    if not total_amount_money_in_atm:
        sleep(1)
        print('We are sorry, but there is no money in the ATM at the moment.\n'
              'Try again later or write to us at fildaiko@gmail.com to speed '
              'up the replenishment of the ATM by a cashier.')
        sleep(1)
        sub_menu(username)

    amount_balance = show_balance(username)
    if not amount_balance:
        sleep(1)
        print(f'\nThe withdrawal operation is not available because your balance is {amount_balance}$.\n'
              f'Replenishment money first.')
        sub_menu(username)

    minimum_multiplicity_of_withdrawal, *_ = min(balance_atm('withdrawal'), key=lambda banknote: banknote[0])
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

    if change_balance(username, -money_withdrawal):
        add_transactions(username, -money_withdrawal, amount_balance)
        sleep(1)
        # change_number_banknotes_when_user_withdraws(money_withdrawal)
        sub_menu(username)


def replenishment_money(username: str) -> None:
    """Allows the user to replenish their balance in an amount that is a multiple of the minimum
        face value of the atm banknote. Part of the money will also be returned to the user if the
        replenishment amount is not a multiple of the minimum face value."""

    amount_balance = show_balance(username)

    minimum_multiplicity_of_replenishment, *_ = min(balance_atm('replenishment'), key=lambda banknote: banknote[0])
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

        final_money_replenishment = money_replenishment - (money_replenishment % minimum_multiplicity_of_replenishment)

        if money_replenishment % minimum_multiplicity_of_replenishment:
            print(f'The amount {money_replenishment % minimum_multiplicity_of_replenishment}$ was not credited '
                  f'to the account and was returned to you')

        change_balance(username, abs(final_money_replenishment))
        add_transactions(username, int(abs(final_money_replenishment)), amount_balance)
        sleep(1)
        sub_menu(username)
