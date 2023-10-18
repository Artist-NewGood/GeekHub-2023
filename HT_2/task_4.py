""" Write a script which accepts a <number> from user and then <number> times asks user for string input.
    At the end script must print out result of concatenating all <number> strings. """

string_count = int(input('Enter number of lines: '))

summary_string = ''

for i in range(1, string_count+1):
    string = input(f'Enter string number {i}: ')
    summary_string += string

print(f'\nSummary string: {summary_string}')
