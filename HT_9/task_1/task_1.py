""" Програма-світлофор.
    Створити програму-емулятор світлофора для авто і пішоходів. Після запуска програми на екран виводиться в
    лівій половині - колір автомобільного, а в правій - пішохідного світлофора. Кожну 1 секунду виводиться
    поточні кольори. Через декілька ітерацій - відбувається зміна кольорів - логіка така сама як і в
    звичайних світлофорах (пішоходам зелений тільки коли автомобілям червоний). """

from time import sleep


def color() -> tuple:
    """Generator to control traffic light colors.
       Returns tuples with colors for car and pedestrians."""

    colors = (
              ('green', 'red'),
              ('yellow', 'red'),
              ('red', 'green'),
              ('yellow', 'red')
             )
    while True:
        yield from colors


def traffic_light() -> None:
    """The function iterates through the colors of a traffic light,
    Printing the current colors for both cars and pedestrians."""

    for color_car, color_man in color():
        repeat_count = 2 if color_car == 'yellow' else 5
        for _ in range(repeat_count):
            print(f'{color_car} {color_man}')
            sleep(1)


if __name__ == '__main__':
    traffic_light()
