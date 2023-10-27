""" Ну і традиційно - калькулятор :slightly_smiling_face: Повинна бути 1 ф-цiя, яка б приймала 3 аргументи - один
    з яких операцiя, яку зробити! Аргументи брати від юзера (можна по одному - 2, окремо +, окремо 2;
    можна всі разом - типу 1 + 2). Операції що мають бути присутні: +, -, *, /, %, //, **.
    Не забудьте протестувати з різними значеннями на предмет помилок! """


class IncorrectCalculateOperation(Exception):
    pass


def calculator(x, action, y):
    try:
        match action:
            case '+':
                return f'\nResult: {x + y}'
            case '-':
                return f'\nResult: {x - y}'
            case '*':
                return f'\nResult: {x * y}'
            case '/':
                return f'\nResult: {x / y}'
            case '%':
                return f'\nResult: {x % y}'
            case '//':
                return f'\nResult: {x // y}'
            case '**':
                return f'\nResult: {x ** y}'
    except ZeroDivisionError:
        return 'Error, cannot be divided by zero'


def check_number(prompt):
    while True:
        num = input(prompt)
        try:
            return int(num)
        except ValueError:
            try:
                return float(num)
            except ValueError:
                print('Error, need some number, try again\n')


def check_operation(prompt):
    while True:
        try:
            operator = input(prompt)
            if operator not in ('+', '-', '*', '/', '%', '//', '**'):
                raise IncorrectCalculateOperation('Error, incorrect action, try again\n')
            return operator
        except IncorrectCalculateOperation as err:
            print(err)


if __name__ == '__main__':
    number_x = check_number('Enter first number: ')
    action = check_operation('Enter calculate action (example  +, -, *, /, %, //, **): ')
    number_y = check_number('Enter second number: ')
    result = calculator(number_x, action, number_y)
    print(result)