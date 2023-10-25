""" Create a Python script that takes an age as input. If the age is less than 18 or greater than 120,
    raise a custom exception called InvalidAgeError. Handle the InvalidAgeError by displaying an
    appropriate error message. """


class InvalidAgeError(Exception):
    pass


age = int(input('Enter your age: '))

try:
    if not 17 < age < 121:
        raise InvalidAgeError('Error, show your passport!')
except InvalidAgeError as err:
    print(err)