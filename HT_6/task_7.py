""" Написати функцію, яка приймає на вхід список (через кому), підраховує кількість однакових елементів у ньомy
    і виводить результат. Елементами списку можуть бути дані будь-яких типів.

    Наприклад:
    1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2] ----> "1 -> 3, foo -> 2, [1, 2] -> 2, True -> 1" """

from collections import Counter


def same_elements(data: list):
    if validation_data(data):
        transformed_data = map(str, data)
        count_elements = Counter(transformed_data)
        return count_elements


def validation_data(sequence_elements):
    try:
        if not isinstance(sequence_elements, list):
            raise TypeError
        return True
    except TypeError:
        print('Error, the required data type is a list')
        exit()


if __name__ == '__main__':
    result = same_elements([1, 1, 'foo', [1, 2], True, 'foo', 1, [1, 2]])

    for key, value in result.items():
        print(f'{key} -> {value},', end=' ')
