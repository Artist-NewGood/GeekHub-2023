import os
from time import sleep
from HT_10.ATM_version_2.incasator.incasator import information_about_users, user_transactions
from HT_10.ATM_version_2.atm.balance import balance_atm, change_balance_atm
from HT_10.ATM_version_2.atm.transactions import show_atm_balance_transactions
from HT_10.ATM_version_2.main import sub_menu, start


class IncorrectDenominationBanknote(Exception):
    pass


class IncorrectNumberBanknotesWithdrawal(Exception):
    pass


def incasator_menu(username: str) -> None:
    """Incasator (admin) menu for using the program"""

    while True:
        print(f'\n____________________\n'
              f'Incasator menu:\n'
              f'𝟏. Information about users\n'
              f'2. Users transactions\n'
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
                information_about_users(username)
                sub_menu(username)
            case '2':
                sleep(1)
                user_transactions(username)

                sub_menu(username)
            case '3':
                sleep(1)
                balance_atm()
                sub_menu(username)
            case '4':
                sleep(1)
                change_balance_atm(username)
                sub_menu(username)
            case '5':
                sleep(1)
                show_atm_balance_transactions()
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
