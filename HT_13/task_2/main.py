""" Створіть за допомогою класів та продемонструйте свою реалізацію шкільної бібліотеки (включіть фантазію).
    Наприклад вона може містити класи Person, Teacher, Student, Book, Shelf, Author, Category і.т.д."""

import os
import sqlite3
from prettytable import PrettyTable


class System:
    def __init__(self):
        pass

    @staticmethod
    def start():
        print('Ласкаво просимо до бібліотеки.')

        print(f'1. Новий читач\n'
              f'2. Відвідувач\n'
              f'\n'
              f'0. Вихід')

        while True:
            menu_item = input('\nВаш вибір: ')
            match menu_item:
                case '1':
                    User.add_new_user()
                case '2':
                    User.login()
                case '0':
                    print('Bye')
                    exit()
                case _:
                    print(' ! Помилка номеру операції(потрібно 1, 2 чи 0)\n')

    @staticmethod
    def user_menu(username: str):
        while True:
            print(f'\n____________________\n'
                  f'Меню:\n'
                  f'𝟏. Взяти книгу\n'
                  f'𝟐. Повернути книгу\n'
                  f'𝟑. Мої взяті книги\n'
                  f'\n'
                  f'𝟎. Завершення роботи\n'
                  f'𝟗. Вихід\n'
                  f'▼')

            match input('Ваш вибір: '):
                case '1':
                    System.take_books_menu(username)
                case '2':
                    Books.back_book(username)
                case '3':
                    User.my_taken_books(username)
                case '0':
                    print('\n♥ Допобачення ♥')
                    exit()
                case '9':
                    print('♥ Допобачення ♥\n')
                    os.system('cls' if os.name == 'nt' else 'clear')
                    System.start()
                case _:
                    print(' ! Невірний номер меню, спробуйте ще раз\n')

    @staticmethod
    def sub_menu(username: str) -> None:
        """Sub menu for the user"""

        print('▼\n'
              '1. Назад до головного меню\n'
              '0. Завершення роботи')

        match input('Ваш вибір: '):
            case '1':
                System.user_menu(username)
            case '0':
                print('\n♥ Допобачення ♥')
                exit()
            case _:
                print(' ! Невірний номер меню, спробуйте ще раз\n')
                System.sub_menu(username)

    @staticmethod
    def check_file() -> str:
        """Checking a file for existence on a given path"""

        full_path = os.path.join(os.getcwd(), 'library.db')

        try:
            with open(full_path, 'r') as db:
                return full_path
        except FileNotFoundError as error:
            print(error)
            exit()

    @staticmethod
    def take_books_menu(username: str):
        while True:
            print(f'\n____________________\n'
                  f'Вибір книги:\n'
                  f'𝟏. За рейтингом\n'
                  f'𝟐. За авторои\n'
                  f'𝟑. За жанром\n'
                  f'𝟒. За роком випуску\n'
                  f'\n'
                  f'0. Назад\n'
                  f'▼')

            match input('Your choice: '):
                case '1':
                    Books.book_selection_options(username, 1)
                case '2':
                    Books.book_selection_options(username, 2)
                case '3':
                    Books.book_selection_options(username, 3)
                case '4':
                    Books.book_selection_options(username, 4)
                case '0':
                    System.user_menu(username)
                case _:
                    print(' ! Невірний номер меню, спробуйте ще раз\n')

    @staticmethod
    def check_input_user_data(prompt: str) -> float | bool:

        while True:
            try:
                number = input(prompt)
                if not number:
                    return False
                return int(number)
            except ValueError:
                print('Потрібно ввести число\n')


class User:
    def __init__(self):
        pass

    @staticmethod
    def login():
        """"""

        username = input('Введіть ваше ім`я: ')

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            query = cursor.execute("""SELECT name
                                FROM library_user
                                WHERE name = ?""",
                                   (username,)).fetchone()

            if not query:
                print(' ! Помилка, користувача з таким іменем нема в базі')
                exit()
            System.user_menu(username)

    @staticmethod
    def my_taken_books(username: str) -> None:
        """"""

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            taken_books = cursor.execute("""SELECT taken_books
                                          FROM library_user
                                          WHERE name = ?""",
                                         (username,)).fetchone()

            if not taken_books[0]:
                print('Нажаль ви ще не брали ні однієї книжки.')
                System.sub_menu(username)

            taken_books = [(book + ' ',) for book in ', '.join(taken_books).split(';') if book]
            table = PrettyTable()
            table.field_names = ['Номер', 'Назва книжки']
            for number, book in enumerate(taken_books, 1):
                table.add_row((number,) + book)

            print(table)
            System.sub_menu(username)

    @staticmethod
    def add_new_user() -> None:
        """"""

        print('Registration')
        username = input('Введіть ваше ім`я: ')
        surname = input('Введіть ваше прізвище: ')
        favourite_genres = input('Введіть ваші улюблені жанри книжок через кому: ')

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            cursor.execute("""INSERT INTO library_user
                                      ('name', 'surname', 'favorite_genre', 'taken_books')
                                      VALUES (?, ?, ?, ?)""",
                           (username, surname, favourite_genres, ''))
            db.commit()
            print('Ласкаво просимо')
            System.user_menu(username)


class DataBase:
    def __init__(self):
        pass

    @staticmethod
    def queries(number: int) -> list:
        """"""

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            if number == 1:
                query_rating = cursor.execute("""SELECT *
                                                  FROM library_books
                                                  ORDER BY rating DESC""").fetchall()
                return query_rating

            elif number == 2:
                query_author = cursor.execute("""SELECT *
                                                             FROM library_books
                                                             ORDER BY author""").fetchall()
                return query_author

            elif number == 3:
                query_genre = cursor.execute("""SELECT *
                                                             FROM library_books
                                                             ORDER BY genre""").fetchall()
                return query_genre

            elif number == 4:
                query_year_release = cursor.execute("""SELECT *
                                                             FROM library_books
                                                             ORDER BY year_release""").fetchall()
                return query_year_release


class Books:
    def __init__(self):
        pass

    @staticmethod
    def book_selection_options(username: str, number: int) -> None:
        """"""

        query = DataBase.queries(number)
        table = PrettyTable()
        table.field_names = ['Номер', 'Рейтинг', 'Автор', 'Назва книги', 'Жанр', 'Рік випуску']
        for number, book in enumerate(query, 1):
            table.add_row((number,) + book)

        print(table)
        while True:
            number_take_book = System.check_input_user_data('Введіть номер книжки, яку хочете взяти '
                                                            '(чи натисніть "Enter" для відміни операції): ')

            if not number_take_book:
                print('Відміна операції')
                System.sub_menu(username)

            if int(number_take_book) not in range(1, len(query) + 1):
                print('Невірний номер книжки, спробуйте ще раз\n')
                continue
            break

        book = ', '.join(query[int(number_take_book) - 1][1:3])
        Books.add_taken_book_to_user(username, book)
        print('Виконано')
        System.sub_menu(username)

    @staticmethod
    def add_taken_book_to_user(username: str, book: str) -> None:
        """"""

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            taken_books = ', '.join(cursor.execute("""SELECT taken_books
                              FROM library_user
                              """).fetchone())
            total = taken_books + '; ' + book if taken_books else book

            cursor.execute("""UPDATE library_user
                                            SET taken_books = ?
                                            WHERE name =?""",
                           (total, username))
            db.commit()

    @staticmethod
    def back_book(username: str) -> None:
        """"""

        full_path = System.check_file()
        with sqlite3.connect(full_path) as db:
            cursor = db.cursor()
            taken_books = cursor.execute("""SELECT taken_books
                                      FROM library_user
                                      WHERE name = ?""",
                                         (username,)).fetchone()
            if not taken_books[0]:
                print('Нажаль ви ще не брали ні однієї книжки')
                System.sub_menu(username)

            taken_books = [(book.strip(' ;'),) for book in ''.join(taken_books).split(';') if book]

            table = PrettyTable()
            table.field_names = ['Номер', 'Назва книжки']
            for number, book in enumerate(taken_books, 1):
                table.add_row((number,) + book)

            print(table)

            while True:
                number_back_book = System.check_input_user_data('Введіть номер книжки, яку хочете повернути '
                                                                '(чи натисніть "Enter" для відміни операції): ')

                if not number_back_book:
                    print('Відміна операції')
                    System.sub_menu(username)

                if int(number_back_book) not in range(1, len(taken_books) + 1):
                    print('Невірний номер книжки, спробуйте ще раз\n')
                    continue

                break
            del taken_books[int(number_back_book) - 1]

            total = '; '.join([name for book in taken_books for name in book])
            cursor.execute("""UPDATE library_user
                                   SET taken_books = ?""",
                           (total,))
            db.commit()
            print('Виконано')
            System.sub_menu(username)


if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent.parent))
    System.start()
