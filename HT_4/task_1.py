""" Написати скрипт, який приймає від користувача два числа (int або float) і робить наступне:
    a. Кожне введене значення спочатку пробує перевести в int. У разі помилки - пробує перевести в float,
       а якщо і там ловить помилку - пропонує ввести значення ще раз (зручніше на даному етапі навчання
       для цього використати цикл while).
    b. Виводить результат ділення першого на друге.
       Якщо при цьому виникає помилка - оброблює її і виводить відповідне повідомлення. """


while True:
    number_1 = input('Enter a first number: ')
    number_2 = input('Enter a second number: ')
    try:
        print(f'Result: {round(int(number_1) / int(number_2), 2)}')
        break
    except ZeroDivisionError:
        print('Error, cannot be divided by zero. Please, try enter numbers one more\n')

    except ValueError:
        try:
            print(f'Result: {round(float(number_1) / float(number_2), 2)}')
            break
        except ZeroDivisionError:
            print('Error, cannot be divided by zero. Please, try enter numbers one more\n')

        except ValueError:
            print('Error, please try enter numbers one more\n')