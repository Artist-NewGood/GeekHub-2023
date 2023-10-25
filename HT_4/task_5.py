""" Create a Python program that repeatedly prompts the user for a number until a valid integer is provided.
    Use a try/except block to handle any ValueError exceptions, and keep asking for input until a valid integer
    is entered. Display the final valid integer. """


flag = True

while flag:
    try:
        num = input('Enter an integer: ')
        if int(num):
            flag = False
    except ValueError:
        if num and '.' not in num:
            print('Error, enter a NUMBER\n')
        else:
            print('Error, enter an INTEGER NUMBER\n')
    else:
        print(f'Your number: {num}')