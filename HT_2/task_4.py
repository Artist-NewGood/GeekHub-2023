""" Write a script which accepts a <number> from user and then <number> times asks user for string input.
    At the end script must print out result of concatenating all <number> strings. """

string_count = int(input('Enter number of lines: '))

summary_string = ''

for i in range(string_count):
    string = input(f'Enter string number {i+1}: ')
    summary_string += string

print(f'\nSummary string: {summary_string}')
