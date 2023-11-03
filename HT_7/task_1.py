""" Створіть функцію, всередині якої будуть записано СПИСОК із п'яти
    користувачів (ім'я та пароль). Функція повинна приймати три аргументи:
    два - обов'язкових (<username> та <password>) і третій - необов'язковий
    параметр <silent> (значення за замовчуванням - <False>).

    Логіка наступна:
        якщо введено правильну пару ім'я/пароль - вертається True;
        якщо введено неправильну пару ім'я/пароль:
            якщо silent == True - функція повертає False
            якщо silent == False - породжується виключення LoginException (його також треба створити =)) """


class LoginException(Exception):
    pass


def check_username_and_login(username: str, password: str, silent: bool = False) -> bool | str:
    """Checking for login and password"""

    user_data = [('Joey', 'polkfrt2#'), ('Brittney', 'qwerty'),
                 ('Alex', 'trAmp'), ('Izabel', 'vbfgjsnwj#22'),
                 ('WhoIAm', 'ukr2023')]

    if (username, password) in user_data:
        return True
    else:
        if silent:
            return False
        raise LoginException('Login error')


if __name__ == '__main__':
    print(check_username_and_login('Joey', 'polkfrt2#'))
    print(check_username_and_login('Joey1', 'polkfrt2#'))
    print(check_username_and_login('Joey1', 'polkfrt2#', silent=True))
