""" Create a custom exception class called NegativeValueError. Write a Python program that takes an integer
    as input and raises the NegativeValueError if the input is negative. Handle this custom exception
    with a try/except block and display an error message. """


class NegativeValueError(Exception):
    pass


num = input('Enter positive number: ')

try:
    if float(num) < 0:
        raise NegativeValueError('Error, number is not positive!')
    print(f'Number: {num}')
except ValueError:
    print('Error, you input incorrect data')
except NegativeValueError as err:
    print(err)