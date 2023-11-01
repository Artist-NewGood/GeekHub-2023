""" Написати функцию <is_prime>, яка прийматиме 1 аргумент - число від 0 до 1000, и яка вертатиме True,
    якщо це число просте і False - якщо ні. """


def is_prime(number):
    number = validation_number(number)
    return number_divisors(number) == 2


def number_divisors(number):
    dividers_count = len([i for i in range(1, number + 1) if number % i == 0])
    return dividers_count


def validation_number(number):
    try:
        if isinstance(number, float):
            raise ValueError
        return int(number)
    except ValueError:
        print('Error, need some an integer number')
        exit()


# if __name__ == '__main__':
    # CASES = ((1, False),
    #          (2, True),
    #          (3, True),
    #          (5, True),
    #          (8, False),
    #          (17, True)
    #          )
    #
    # for case, answer in CASES:
    #     assert is_prime(case) == answer
