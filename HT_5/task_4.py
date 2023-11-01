# """ Наприклад маємо рядок
#     ↓
#     "f98neroi4nr0c3n30irn03ien3c0rfe    kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345"
#
#     Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
#     -  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
#     -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
#     -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)   """
#
#
# from collections import Counter
# import re
#
# def check_string(string):
#     letters = (letter for letter in string if letter.isalpha())
#     digits = (digit for digit in string if digit.isdigit())
#     digits_group_version = re.findall(r'\d+', string)
#
#     if 30 <= len(string) <= 50:
#         print(f'Length of string - {len(string)}\n'
#               f'Number of letters - {sum(1 for _ in letters)}\n'
#               f'Number of digits - {sum(1 for _ in digits)}'
#               )
#
#     elif len(string) < 30:
#         total_digit_sum = sum(map(int, digits))
#         total_digit_sum_group_version = sum(map(int, digits_group_version))
#         print(f'The sum of all numbers - {total_digit_sum}\n'
#               f'The sum of all numbers (group version) - {total_digit_sum_group_version}\n'
#               f'String without digits - {"".join(letters)}')
#
#     else:
#         letter_counts = Counter(letters)
#         for key, value in letter_counts.items():
#             print(f'Letter "{key}" - appears {value} times')
#
#
# if __name__ == "__main__":
#     line = input('Please, enter some string: ')
#     check_string(line)


""" Наприклад маємо рядок
    ↓
    "f98neroi4nr0c3n30irn03ien3c0rfe    kdno400wenwkowe00koijn35pijnp46ij7k5j78p3kj546p4 65jnpoj35po6j345"

    Створіть ф-цiю, яка буде отримувати рядки на зразок цього та яка оброблює наступні випадки:
    -  якщо довжина рядка в діапазонi 30-50 (включно) -> прiнтує довжину рядка, кiлькiсть букв та цифр
    -  якщо довжина менше 30 -> прiнтує суму всiх чисел та окремо рядок без цифр лише з буквами (без пробілів)
    -  якщо довжина більше 50 -> щось вигадайте самі, проявіть фантазію =)   """


from collections import Counter
import re


def check_string(string):
    letters = (letter for letter in string if letter.isalpha())
    digits = (digit for digit in string if digit.isdigit())
    digits_group_version = re.findall(r'\d+', string)

    if 30 <= len(string) <= 50:
        print(f'Length of string - {len(string)}\n'
              f'Number of letters - {sum(1 for _ in letters)}\n'
              f'Number of digits - {sum(1 for _ in digits)}')

    elif len(string) < 30:
        total_digit_sum = sum(map(int, digits))
        total_digit_sum_group_version = sum(map(int, digits_group_version))
        print(f'The sum of all numbers - {total_digit_sum}\n'
              f'The sum of all numbers (group version) - {total_digit_sum_group_version}\n'
              f'String without digits - {"".join(letters)}')

    else:
        letter_counts = Counter(letters)
        for key, value in letter_counts.items():
            print(f'Letter "{key}" - appears {value} times')


if __name__ == "__main__":
    line = input('Please, enter some string: ')
    check_string(line)
