""" Створіть функцію для валідації пари ім'я/пароль за наступними правилами:
       - ім'я повинно бути не меншим за 3 символа і не більшим за 50;
       - пароль повинен бути не меншим за 8 символів і повинен мати хоча б одну
         цифру;
       - якесь власне додаткове правило :)

    Якщо якийсь із параметрів не відповідає вимогам - породити виключення із
    відповідним текстом."""


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
        print('Error, your username is not the right length (need length between 3 and 50)')
    except SpaceInUsername:
        print('Error, no spaces are allowed in the username')


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
        print('Error, your password is too short (must be more than 8 characters)')
    except NoDigitInPassword:
        print('Error, your password must contain at least one digit')
    except NoUpperLettersInPassword:
        print('Error, your password must contain at least one capital letter')


def main(username: str, password: str) -> tuple[str, str]:
    """Main controller"""

    result_username_validation = username_validation(username)
    result_password_validation = password_validation(password)

    return result_username_validation, result_password_validation


if __name__ == '__main__':
    user_name = input('Enter your username for validation: ')
    user_password = input('Enter your password for validation: ')
    result = main(user_name, user_password)
    print(result)
