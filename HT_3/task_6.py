""" Write a script to get the maximum and minimum value in a dictionary. """

dict_data = {'one': 1, 2: 'two', 'three': 3, 'Tom': ' Hanks', True: False, 8: [], 'ten': (3, 4), 'hi': {1, 5}}

dict_values = [val for val in dict_data.values() if not isinstance(val, (str, bool, list, tuple, set, dict))]

print(f'Maximum value in a dictionary: {max(dict_values)}'
      f'\nMinimum value in a dictionary: {min(dict_values)}')