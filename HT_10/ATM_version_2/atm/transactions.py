import sqlite3
from datetime import datetime
from prettytable import PrettyTable


def add_atm_balance_transactions(username: str, banknote: int, before_update: int, after_update: int) -> None:
    """Adds a transaction to the corresponding table to change the atm balance"""

    from HT_10.ATM_version_2.user.utils import check_file

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


def show_atm_balance_transactions() -> None:
    """Displays the data in the form of a table showing all operations
       performed by the cash collector with the atm balance"""

    from HT_10.ATM_version_2.user.utils import check_file

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
