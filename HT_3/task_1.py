""" Write a script that will run through a list of tuples and replace the last value for each tuple.
    The list of tuples can be hardcoded. The "replacement" value is entered by user.
    The number of elements in the tuples must be different. """

list_of_tuples = [(1, 2, 'bar'), (5, 'baz', 7, 19.3), ('geek', 'hub'), (True, 'False', None), ([1, 2], ['1', '2'])]

replacement_value = input('Enter replacement value: ')

for i in range(len(list_of_tuples)):
    list_of_tuples[i] = list(list_of_tuples[i])
    list_of_tuples[i][-1] = replacement_value
    list_of_tuples[i] = tuple(list_of_tuples[i])

print(list_of_tuples)

