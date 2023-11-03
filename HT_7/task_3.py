""" На основі попередньої функції (скопіюйте кусок коду) створити наступний скрипт:
        а) створити список із парами ім'я/пароль різноманітних видів (орієнтуйтесь по
        правилам своєї функції) - як валідні, так і ні;
        б) створити цикл, який пройдеться по цьому циклу і, користуючись валідатором,
        перевірить ці дані і надрукує для кожної пари значень відповідне повідомлення.

        Наприклад:

        Name: vasya
        Password: wasd
        Status: password must have at least one digit
        -----
        Name: vasya
        Password: vasyapupkin2000
        Status: OK

        P.S. Не забудьте використати блок try/except ;)"""


class IncorrectLengthUsername(Exception):
    pass


class SpaceInUsername(Exception):
    pass


class IncorrectLengthUserPassword(Exception):
    pass


class NoDigitInPassword(Exception):
    pass


class NoUpperLettersInPassword(Exception):
    pass


def username_validation(username: str) -> str:
    """Checking the username for compliance with the requirements"""
    try:
        if not 3 <= len(username) <= 50:
            raise IncorrectLengthUsername
        if ' ' in username:
            raise SpaceInUsername
        return 'OK'
    except IncorrectLengthUsername:
        return 'Your username is not the right length (need length between 3 and 50)'
    except SpaceInUsername:
        return 'No spaces are allowed in the username'


def password_validation(password: str) -> str:
    """Checking the password for compliance with the requirements"""
    try:
        if len(password) < 8:
            raise IncorrectLengthUserPassword
        if password.isalpha():
            raise NoDigitInPassword
        if password == password.lower():
            raise NoUpperLettersInPassword
        return 'OK'
    except IncorrectLengthUserPassword:
        return 'Your password is too short (must be more than 8 characters)'
    except NoDigitInPassword:
        return 'Your password must contain at least one digit'
    except NoUpperLettersInPassword:
        return 'Your password must contain at least one capital letter'


def main(username: str, password: str) -> tuple[str, str]:
    """Main controller"""

    result_username_validation = username_validation(username)
    result_password_validation = password_validation(password)

    return result_username_validation, result_password_validation


if __name__ == '__main__':
    user_data = [('Jo', 'Polkfrt2'), ('Brit Spears', 'Qwerty221'),
                 ('Alex', 'tramp'), ('Izabel', 'hrteio21'),
                 ('WIN', 'Ukrainian'), ('Alex_Artist', 'Mamarika2023')]

    for user_name, user_password in user_data:
        print(f'Name: {user_name}\n'
              f'Password: {user_password}\n'
              f'Status: {main(user_name, user_password)[0]}\n'
              f'\t\t{main(user_name, user_password)[1]}\n')
