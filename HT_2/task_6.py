""" Write a script to check whether a value from user input is contained in a group of values.
    e.g. [1, 2, 'u', 'a', 4, True] --> 2 --> True
         [1, 2, 'u', 'a', 4, True] --> 5 --> False """

values_list = ['1', '2', 'u', 'a', '4', 'True']
result = input('Enter value to check: ') in values_list

print(f'Result: {result}')
