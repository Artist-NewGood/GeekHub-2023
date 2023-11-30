""" Create 'list'-like object, but index starts from 1 and index of 0 raises error.
    Тобто це повинен бути клас, який буде поводити себе так, як list (маючи основні методи),
    але індексація повинна починатись із 1 """


class MyList(list):
    def __getitem__(self, index):
        if not index:
            raise IndexError('Index start from 1!')
        return super().__getitem__(index - 1 if index > 0 else index)


if __name__ == '__main__':
    a = MyList([1, 2, 3, 4, 5])
    print(a[1])
    print(a[-1])
    print(a.pop())
    a.append(10)
    print(a)
    print(a[-1])

