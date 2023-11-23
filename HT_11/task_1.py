""" Створити клас Calc, який буде мати атребут last_result та 4 методи.
    Методи повинні виконувати математичні операції з 2-ма числами, а саме додавання, віднімання, множення, ділення.
      - Якщо під час створення екземпляру класу звернутися до атребута last_result він повинен повернути пусте значення.
      - Якщо використати один з методів - last_result повенен повернути результат виконання ПОПЕРЕДНЬОГО методу.

    Example:
    last_result --> None
    1 + 1
    last_result --> None
    2 * 3
    last_result --> 2
    3 * 4
    last_result --> 6
    ...
      - Додати документування в клас (можете почитати цю статтю:
        https://realpython.com/documenting-python-code/ )"""


class Calc:
    """
       Calculator class
       4 methods to calculate 2 values
    """
    def __init__(self):
        self.last_result = None
        self.result = None
        self.current_result = None

    def add(self, number_1, number_2):
        self.result = number_1 + number_2
        self.operation()
        return self.result
        
    def multi(self, number_1, number_2):
        self.result = number_1 * number_2
        self.operation()
        return self.result
        
    def sub(self, number_1, number_2):
        self.result = number_1 - number_2
        self.operation()
        return self.result
        
    def div(self, number_1, number_2):
        try:
            self.result = number_1 / number_2
        except ZeroDivisionError as err:
            self.result = err
        self.operation()
        return self.result
    
    def operation(self):
        self.last_result = self.current_result
        self.current_result = self.result


if __name__ == '__main__':
    equation = Calc()
    print(equation.last_result)
    equation.add(1, 1)
    print(equation.last_result)
    equation.multi(2, 3)
    print(equation.last_result)
    equation.multi(3, 3)
    print(equation.last_result)



