""" Користувач вводить змiннi "x" та "y" з довiльними цифровими значеннями. 
    Створiть просту умовну конструкцiю (звiсно вона повинна бути в тiлi ф-цiї), пiд час виконання якої 
    буде перевiрятися рiвнiсть змiнних "x" та "y" та у випадку нервіності - виводити ще і різницю.
    Повиннi опрацювати такi умови (x, y, z заміність на відповідні числа):
    x > y;       вiдповiдь - "х бiльше нiж у на z"
    x < y;       вiдповiдь - "у бiльше нiж х на z"
    x == y.      вiдповiдь - "х дорiвнює z """


def difference_of_numbers(x, y):
    diff = round(abs(x - y), 2)
    if x > y:
        return f'\nAnswer: Число {x} більше ніж число {y} на {diff}'
    elif x < y:
        return f'\nAnswer: Число {y} більше ніж число {x} на {diff}'
    elif x == y:
        return f'\nAnswer: Число {x} дорівнює числу {y}'


def check_x_and_y(prompt):
    while True:
        number = input(prompt)
        try:
            return int(number)
        except ValueError:
            try:
                return float(number)
            except ValueError:
                print('Incorrect input data. Please, enter a number\n')


if __name__ == "__main__":
    number_x = check_x_and_y('Please, enter number X: ')
    number_y = check_x_and_y('Please, enter number Y: ')
    result = difference_of_numbers(number_x, number_y)
    print(result)