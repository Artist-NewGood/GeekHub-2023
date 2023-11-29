""" Створіть клас в якому буде атребут який буде рахувати кількість створених екземплярів класів. """


class Count:
    count = 0

    def __init__(self, name):
        self.name = name
        self.__class__.count += 1


if __name__ == '__main__':
    a = Count('a')
    b = Count('b')
    c = Count('c')

    print(c.count)
