""" Write a script to remove values duplicates from dictionary. Feel free to hardcode your dictionary. """

dict1 = {1: 'one', 2: 'two', 3: 'three', 4: 'three', 5: 'five', 6: 'five'}

dict2 = {}

for key, value in dict1.items():
    if value not in dict2.values():
        dict2[key] = value

dict1 = dict2.copy()
dict2.clear()

print(dict1)







