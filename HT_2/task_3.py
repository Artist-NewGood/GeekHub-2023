""" Write a script which accepts a <number> from user and print out a sum of the first <number> positive integers. """

number = int(input('Enter number: '))
result = sum(range(1, number+1))

print(f'Result: {result}')
