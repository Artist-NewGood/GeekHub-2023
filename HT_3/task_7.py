""" Write a script which accepts a <number> from user and generates dictionary in range <number>
    where key is <number> and value is <number>*<number>
    e.g. 3 --> {0: 0, 1: 1, 2: 4, 3: 9} """

dict_number = {i: i ** 2 for i in range(int(input('Enter a number: ')))}

print(f'You dictionary: {dict_number}')