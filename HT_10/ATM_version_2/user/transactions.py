import sqlite3
from typing import Any
from HT_10.ATM_version_2.user.utils import check_file
from prettytable import PrettyTable
from datetime import datetime


def show_transactions(username: str, option=1) -> list[Any]:
    """Viewing user transactions from a database as a formatted table"""

    full_path = check_file()
    with sqlite3.connect(full_path) as db:
        cursor = db.cursor()

        cursor.execute("""SELECT Operation, Amount, Balance_after, Date 
                          FROM users_transactions
                          WHERE login == ?""",
                       (username,))

        if option:
            data_operations = cursor.fetchall()

            table = PrettyTable()
            table.field_names = ['Operation', 'Amount', 'Balance_after', 'Date']

            for i in data_operations:
                table.add_row(i)

            print('\n***                     TRANSACTIONS                         ***')
            print(table)

        return data_operations


def add_transactions(username: str, funds: int, balance: int) -> None:
    """Adding a user transaction to the appropriate table in the database"""

    full_path = check_file()
    if funds:
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO users_transactions ('login', 'Operation', 
                                                                    'Amount', 'Balance_after', 'Date')
                              VALUES (?, ?, ?, ?, ?)""",
                           (username, "Withdrawal" if funds < 0 else "Replenishment", abs(funds),
                            balance + funds, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            db.commit()
