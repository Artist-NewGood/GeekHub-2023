""" Всі ви знаєте таку функцію як <range>. Напишіть свою реалізацію цієї функції.
    Тобто щоб її можна було використати у вигляді:

    for i in my_range(1, 10, 2):
        print(i)
    1
    3
    5
    7
    9
   P.S. Повинен вертатись генератор.
   P.P.S. Для повного розуміння цієї функції - можна почитати документацію по ній:
   https://docs.python.org/3/library/stdtypes.html#range
   P.P.P.S Не забудьте обробляти невалідні ситуації (аналог range(1, -10, 5)).
   Подивіться як веде себе стандартний range в таких випадках."""


def my_range(start, end=None, step=1):
    """Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step"""

    if not isinstance(start, int) or not isinstance(end, (int, type(None))) or not isinstance(step, int):
        raise TypeError(f'{type(start).__name__} object cannot be interpreted as an integer')

    if end is None:
        start, end = 0, start

    while (start < end and step > 0) or (start > end and step < 0):
        yield start
        start += step


