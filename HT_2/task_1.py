""" Write a script which accepts a sequence of comma-separated numbers from user 
    and generate a list and a tuple with those numbers. """

list_of_numbers = [num.strip('" "') for num in input('Enter numbers separated by commas: ').split(',')]
convert_numbers_to_integer = list(map(int, list_of_numbers))
tuple_of_integer_numbers = tuple(convert_numbers_to_integer)

print(f'List of numbers: {convert_numbers_to_integer}')
print(f'Tuple of numbers: {tuple_of_integer_numbers}')
