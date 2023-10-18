""" Write a script to concatenate all elements in a list into a string and print it.
    List must be included both strings and integers and must be hardcoded."""

list_data = [1, 2, 5, 65654, 'hi', 'hello', 'geeknub', True, False, None, 3.5, 7.84]
string = ''.join(map(str, list_data))

print(f'Result: {string}')
