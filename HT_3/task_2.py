""" Write a script to remove an empty elements from a list.
    Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []] """


test_list = [(), 'hey', ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]

test_list = [value for value in test_list if value]

print(test_list)