""" Write a Python program that demonstrates exception chaining. Create a custom exception class
    called CustomError and another called SpecificError. In your program (could contain any logic you want),
    raise a SpecificError, and then catch it in a try/except block, re-raise it as a CustomError with the
    original exception as the cause. Display both the custom error message and the original exception message. """


class CustomError(Exception):
    pass


class SpecificError(Exception):
    pass


line = input('Enter word: ')

try:
    if line.isdigit():
        raise SpecificError('Error, Need symbol word')
except SpecificError as err:
    try:
        raise CustomError('Error, need only alphabet symbol') from err
    except CustomError as err1:
        print(err1)
        print(err)