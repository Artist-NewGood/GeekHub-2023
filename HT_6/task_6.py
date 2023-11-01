""" Написати функцію, яка буде реалізувати логіку циклічного зсуву елементів в списку.
    Тобто функція приймає два аргументи: список і величину зсуву (якщо ця величина додатня - пересуваємо з кінця
    на початок, якщо від'ємна - навпаки - пересуваємо елементи з початку списку в його кінець).

    Наприклад:
    fnc([1, 2, 3, 4, 5], shift=1) --> [5, 1, 2, 3, 4]
    fnc([1, 2, 3, 4, 5], shift=-2) --> [3, 4, 5, 1, 2] """


def displacement_of_elements(data, shift):
    shift = validation_shift(shift)
    shift %= len(data)

    if not validation_data(data):
        return f'Data type must be a list'

    if shift > 0:
        return data[-shift:] + data[:-shift]
    else:
        return data[-shift:] + data[:-shift]


def validation_shift(number):
    try:
        if isinstance(number, float):
            raise ValueError
        return int(number)
    except ValueError:
        print('Error, need some an integer number')
        exit()


def validation_data(sequence_numbers):
    try:
        return isinstance(sequence_numbers, list)
    except ValueError:
        print('Error, the required data type is a list')


if __name__ == '__main__':
    CASES = (([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5]),
             ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),
             ([1, 2, 3, 4, 5], -3, [4, 5, 1, 2, 3]),
             ([1, '2', True, [1, 2], ()], 6, [(), 1, '2', True, [1, 2]]),
             ([1, '2', True, [1, 2], ()], -17, [True, [1, 2], (), 1, '2']),
             ([1, '2', True, [1, 2], ()], 8, [True, [1, 2], (), 1, '2']),
             )
    for case_1, case_2, answer in CASES:
        assert displacement_of_elements(case_1, case_2) == answer
