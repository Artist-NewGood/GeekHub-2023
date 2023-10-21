""" Write a script that will run through a list of tuples and replace the last value for each tuple.
    The list of tuples can be hardcoded. The "replacement" value is entered by user.
    The number of elements in the tuples must be different. """

list_of_tuples = [(1, 5, True), ("aaa", 2), (0,), ()]
print(f'Original list: {list_of_tuples}')

replacement_value = input('Enter replacement value: ')

for i in range(len(list_of_tuples)):
    if len(list_of_tuples[i]) != 0:
        list_of_tuples[i] = list(list_of_tuples[i])
        list_of_tuples[i][-1] = replacement_value
        list_of_tuples[i] = tuple(list_of_tuples[i])

print(f'Changed list: {list_of_tuples}')
