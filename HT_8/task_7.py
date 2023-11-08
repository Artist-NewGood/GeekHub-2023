""" Напишіть функцію, яка приймає 2 списки. Результатом має бути новий список, в якому знаходяться
    елементи першого списку, яких немає в другому. Порядок елементів, що залишилися має відповідати
    порядку в першому (оригінальному) списку. Реалізуйте обчислення за допомогою генератора.

    Приклад:
    array_diff([1, 2], [1]) --> [2]
    array_diff([1, 2, 2, 2, 4, 3, 4], [2]) --> [1, 4, 3, 4] """

from typing import Any


def get_unique_elements(data_1: list[Any], data_2: list[Any]) -> list[Any]:
    """Creates a new list that contains  elements of the first list that are not in the second"""
    unique_elements = (
                       elem
                       for elem in data_1
                       if elem not in data_2
                      )

    return list(unique_elements)


if __name__ == '__main__':
    CASES = (
        ([1, 2, 4, 7, 9], [1, 4, 9], [2, 7]),
        ([2, 6, 4, 7, 9], [1, 4, 9], [2, 6, 7]),
        ([1, 2, 3, 4, 8], [8, ], [1, 2, 3, 4]),
        ([5, 25, 0], [0, 5, 25], []),
    )

    for case_1, case_2, answer in CASES:
        assert get_unique_elements(case_1, case_2) == answer
