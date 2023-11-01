""" Написати функцію <fibonacci>, яка приймає один аргумент і виводить всі числа Фібоначчі, що не перевищують його. """


def fibonacci(limiter, num_1=0, num_2=1):
    fibonacci_number = []

    for i in range(limiter):
        num_1, num_2 = num_2, num_1 + num_2
        if num_1 >= limiter:
            break
        fibonacci_number.append(num_1)
    return fibonacci_number


def validation_data_type(prompt):
    number = input(prompt)
    try:
        return int(number)
    except ValueError:
        print('Error, need some an integer number')
        exit()


if __name__ == '__main__':
    limiter_number = validation_data_type('Enter some integer number: ')
    result = fibonacci(limiter_number)
    print('Fibonacci sequence:', *result)
