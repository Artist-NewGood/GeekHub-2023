""" Write a script which accepts two sequences of comma-separated colors from user. 
    Then print out a set containing all the colors from color_list_1 which are not present in color_list_2 """

color_list_1 = [color.strip(" ") for color in input('First sequence of colors, separated by commas: ').split(',')]
color_list_2 = [color.strip(" ") for color in input('Second sequence of colors, separated by commas: ').split(',')]

print(f'Result: {set(color_list_1).difference(set(color_list_2))}')
