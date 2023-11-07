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


def my_range(*args):
    """Return an object that produces a sequence of integers from start (inclusive) to stop (exclusive) by step"""
    if not len(args):
        raise TypeError('range expected at least 1 argument, got 0')

    if not any(isinstance(number, int) for number in args):
        raise TypeError(f'{str(type(*args))[7:-1]} object cannot be interpreted as an integer')

    if len(args) > 3:
        raise TypeError(f'range expected at most 3 arguments, got {len(args)}')

    if len(args) == 1:
        start, end, step = 0, args[0], 1
    elif len(args) == 2:
        start, end, step = args[0], args[1], 1
    else:
        start, end, step = args

    while (start < end and step > 0) or (start > end and step < 0):
        yield start
        start += step
