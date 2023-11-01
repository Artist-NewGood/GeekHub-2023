""" Написати функцію <prime_list>, яка прийматиме 2 аргументи - початок і кінець діапазона, і вертатиме
    список простих чисел всередині цього діапазона. Не забудьте про перевірку на валідність введених даних
    та у випадку невідповідності - виведіть повідомлення. """


def prime_list(start: int, end: int) -> list[int]:
    prime_dict = {}

    for number in range(start, end + 1):
        number_of_divisors = len(count_of_divisors(number))

        if number_of_divisors == 2:
            prime_dict.setdefault('Prime numbers', []).append(number)

    return prime_dict.get('Prime numbers', 'Empty')


def count_of_divisors(number: int) -> list[int]:
    number_of_divisors = []
    for divider in range(1, number + 1):
        if number % divider == 0:
            number_of_divisors.append(number)
    return number_of_divisors


def validation_range(number: str) -> int:
    try:
        return int(number)
    except ValueError:
        print('Error, need some an integer number')
        exit()


if __name__ == '__main__':
    start_range = validation_range(input('Please, enter start of the range: '))
    end_range = validation_range(input('Please, enter end of the range: '))
    result = prime_list(start_range, end_range)
    print(f'\nPrime number list: {result}')
