"""" Банкомат 3.0
    - реалізуйте видачу купюр за логікою видавання найменшої кількості купюр.
    Наприклад: 2560 --> 2х1000, 1х500, 3х20. Будьте обережні з "жадібним алгоритмом"! """


import os
from time import sleep


def user_menu(username: str) -> None:
    """User menu for using the program"""

    from HT_12.ATM_version_4.user.user_module import User
    from HT_12.ATM_version_4.atm.atm_module import ATM
    from HT_12.ATM_version_4.system.system_module import show_transactions

    while True:
        print(f'\n____________________\n'
              f'Menu:\n'
              f'𝟏. Withdrawal\n'
              f'𝟐. Replenish money\n'
              f'𝟑. Show balance\n'
              f'𝟒. Transactions\n'
              f'\n'
              f'Additional features\n'
              f'𝟓. Transfer money to another user\n'
              f'𝟔. Deposit money (🔥 offer)\n'
              f'\n'
              f'𝟎. Exit\n'
              f'𝟗. Log out\n'
              f'▼')

        match input('Your choice: '):
            case '1':
                User.withdrawal(username)
            case '2':
                User.replenishment_money(username)
            case '3':
                sleep(1)
                print(f'--------------\n'
                      f'Money on your balance: {User.show_balance(username)}$')
                sub_menu(username)
            case '4':
                sleep(1)
                show_transactions(username)
                sub_menu(username)
            case '5':
                sleep(1)
                ATM.transfer_money(username)
            case '6':
                sleep(1)
                ATM.deposit_money(username)
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


def verification_animation() -> None:
    """Displays an animation of waiting for data verification"""

    print('Check', end='', flush=True)
    for _ in range(3):
        sleep(1)
        print('.', end='', flush=True)
    return


def deposit_time_animation(years: int):
    """"""

    sleep(1)
    print('\nTime is began', end='', flush=True)
    for year in range(1, years+1):
        for _ in range(3):
            sleep(1)
            print('.', end='', flush=True)
        sleep(1)
        print(f' {year} year ', end='', flush=True)
    return


def sub_menu(username: str) -> None:
    """Sub menu for the user"""

    from HT_12.ATM_version_4.incasator.incasator_module import Incasator

    print('▼\n'
          '1. Back to main menu\n'
          '0. Exit')

    match input('Your choice: '):
        case '1':
            sleep(1)
            if username != 'admin':
                user_menu(username)
            Incasator.incasator_menu(username)
        case '0':
            print('\n♥ Bye ♥')
            exit()
        case _:
            print(' ! Error number, try again\n')
            sleep(1)
            sub_menu(username)


def start() -> None:
    """Main controller"""

    from HT_12.ATM_version_4.user.user_module import User
    from HT_12.ATM_version_4.system.system_module import add_new_users, check_login_data

    print('▼\n'
          'Here are the available features of this ATM.\n'
          ' • withdraw money from your account\n'
          ' • replenishment money to your account\n'
          ' • view your account transactions\n'
          'If you are not our client, you can register '
          '(you will need to come up with a username and a "good" password).\n'
          'After that, you will also have access to the full functionality of the ATM.')

    while True:
        print('\n--------------------\n'
              'Choose what you want\n'
              '𝟙. Registration\n'
              '𝟚. Log in\n'
              '\n'
              '𝟎. Exit\n'
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
                        user_menu(result_check_users_name)
                    if i > 1:
                        print(f'You have {i - 1} more  tries')
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
                print(' ! Error. Please, enter a correct number operation (1, 2 or 0). Try again')
                sleep(1)


if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent.parent))
    start()

