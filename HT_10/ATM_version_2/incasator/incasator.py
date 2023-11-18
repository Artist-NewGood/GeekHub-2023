import sqlite3
from prettytable import PrettyTable
from HT_10.ATM_version_2.main import sub_menu
from time import sleep


def information_about_users(username: str) -> None:
    """Displays general information about all atm users"""

    from HT_10.ATM_version_2.user.utils import check_file

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


def user_transactions(username: str) -> None:
    """Displays information about all transactions of atm users on the screen"""

    print('----------------'
          '\nWhat kind of operations do you want to make?\n'
          '1. Transactions of all users\n'
          '2. Search transactions by user\n'
          '\n'
          '0. Back to main menu\n'
          '▼')

    from HT_10.ATM_version_2.user.utils import check_file
    from HT_10.ATM_version_2.incasator.utils import incasator_menu

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
                        sleep(1)
                        search_user = input('Input username (or press "Enter" to cancel): ')
                        if not search_user:
                            sleep(1)
                            print('❎ Cancel operation')

                            sub_menu(username)

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
                    incasator_menu(username)
                case _:
                    print(' ! Error number, try again\n')
                    sleep(1)
                    # sub_menu(username)
