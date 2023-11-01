""" Написати функцію <square>, яка прийматиме один аргумент - сторону квадрата, і вертатиме 3 значення
    у вигляді кортежа: периметр квадрата, площа квадрата та його діагональ. """

from math import sqrt


def square(side):
    side = validation_data_type(side)
    perimeter = side * 4
    area = round(side ** 2, 2)
    diagonal = round(side * sqrt(2), 2)
    return perimeter, area, diagonal


def validation_data_type(number):
    try:
        return float(number)
    except ValueError:
        print('Error, need some number')
        exit()


if __name__ == '__main__':
    CASES = (
            (1, (4, 1, 1.41)),
            (2, (8, 4, 2.83)),
            (5, (20, 25, 7.07)),
            (7.7, (30.8, 59.29, 10.89))
    )

    for case, answer in CASES:
        assert square(case) == answer
