"""" Банкомат 2.0
    - усі дані зберігаються тільки в sqlite3 базі даних у відповідних таблицях.
    Більше ніяких файлів. Якщо в попередньому завданні ви добре продумали
    структуру програми то у вас не виникне проблем швидко адаптувати її до нових вимог.

    - на старті додати можливість залогінитися або створити нового користувача
    (при створенні нового користувача, перевіряється відповідність логіну і паролю
    мінімальним вимогам. Для перевірки створіть окремі функції)

    - в таблиці з користувачами також має бути створений унікальний користувач-інкасатор,
    який матиме розширені можливості (домовимось, що логін/пароль будуть admin/admin щоб
    нам було простіше перевіряти)

    - банкомат має власний баланс

    - кількість купюр в банкоматі обмежена (тобто має зберігатися номінал та кількість).
    Номінали купюр - 10, 20, 50, 100, 200, 500, 1000

    - змінювати вручну кількість купюр або подивитися їх залишок в банкоматі може лише інкасатор

    - користувач через банкомат може покласти на рахунок лише суму кратну мінімальному номіналу
    що підтримує банкомат. В іншому випадку - повернути "здачу"
    (наприклад при поклажі 1005 --> повернути 5). Але це не має впливати на баланс/кількість
    купюр банкомату, лише збільшується баланс користувача (моделюємо наявність двох незалежних
    касет в банкоматі - одна на прийом, інша на видачу)

    - зняти можна лише в межах власного балансу, але не більше ніж є всього в банкоматі.

    - при неможливості виконання якоїсь операції - вивести повідомлення з причиною
    (невірний логін/пароль, недостатньо коштів на рахунку,
    неможливо видати суму наявними купюрами тощо.)

    - файл бази даних з усіма створеними таблицями і даними також додайте в репозиторій,
    що б ми могли його використати """


import os
from time import sleep


def user_menu(username: str) -> None:
    """User menu for using the program"""

    from HT_10.ATM_version_2.user.balance import withdrawal, show_balance, replenishment_money
    from HT_10.ATM_version_2.user.transactions import show_transactions

    while True:
        print(f'\n____________________\n'
              f'Menu:\n'
              f'𝟏. Withdrawal\n'
              f'𝟐. Replenish money\n'
              f'𝟑. Show balance\n'
              f'𝟒. Transactions\n'
              f'\n'
              f'𝟎. Exit\n'
              f'𝟗. Log out\n'
              f'▼')

        match input('Your choice: '):
            case '1':
                withdrawal(username)
            case '2':
                replenishment_money(username)
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


def sub_menu(username: str) -> None:
    """Sub menu for the user"""

    from HT_10.ATM_version_2.incasator.utils import incasator_menu

    print('▼\n'
          '1. Back to main menu\n'
          '0. Exit')

    match input('Your choice: '):
        case '1':
            sleep(1)
            if username != 'admin':
                user_menu(username)
            incasator_menu(username)
        case '0':
            print('\n♥ Bye ♥')
            exit()
        case _:
            print(' ! Error number, try again\n')
            sleep(1)
            sub_menu(username)


def start() -> None:
    """Main controller"""

    from HT_10.ATM_version_2.user.utils import check_login_data
    from HT_10.ATM_version_2.user.new_user import add_new_users

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
                print(' ! Error. Please, enter a correct number operation (1, 2 or 0). Try again')
                sleep(1)


if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent.parent))
    start()
