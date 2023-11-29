""" Напишіть програму, де клас «геометричні фігури» (Figure) містить властивість color з початковим
    значенням white і метод для зміни кольору фігури, а його підкласи «овал» (Oval) і «квадрат» (Square)
    містять методи __init__ для завдання початкових розмірів об'єктів при їх створенні. """


class Figure:
    def __init__(self):
        self.color = 'white'

    def change_color(self, color):
        self.color = color


class Oval(Figure):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius


class Square(Figure):
    def __init__(self, side):
        super().__init__()
        self.side = side


if __name__ == '__main__':
    print('Oval:')
    oval_1 = Oval(5)
    print(oval_1.color)

    oval_1.change_color('black')
    print(oval_1.color)

    print('\nSquare:')
    square_1 = Square(3)
    print(square_1.color)
