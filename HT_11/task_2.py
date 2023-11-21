""" Створити клас Person, в якому буде присутнім метод __init__ який буде приймати якісь аргументи,
    які зберігатиме в відповідні змінні.
    - Методи, які повинні бути в класі Person - show_age, print_name, show_all_information.
    - Створіть 2 екземпляри класу Person та в кожному з екземплярів створіть атрибут profession
      (його не має інсувати під час ініціалізації)."""


class Person:
    def __init__(self, age, name):
        self.age = age
        self.name = name

    def show_age(self):
        print(self.age)

    def print_name(self):
        print(self.name)

    def show_all_information(self):
        print(self.__dict__)


if __name__ == '__main__':
    Alex = Person(18, 'Alex')
    John = Person(25, 'John')

    Alex.profession = 'Programming'
    John.profession = 'Doctor'

    Alex.show_all_information()
    John.show_all_information()
