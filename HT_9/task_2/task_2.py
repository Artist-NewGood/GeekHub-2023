""" Написати функцію, яка приймає два параметри: ім'я (шлях) файлу та кількість символів.
    Файл також додайте в репозиторій. На екран має бути виведений список із трьома блоками - символи з початку,
    із середини та з кінця файлу. Кількість символів в блоках - та, яка введена в другому параметрі.
    Придумайте самі, як обробляти помилку, наприклад, коли кількість символів більша, ніж є в файлі або,
    наприклад, файл із двох символів і треба вивести по одному символу, то що виводити на місці
    середнього блоку символів?). Не забудьте додати перевірку чи файл існує. """

from typing import Tuple, List
import os


def validate_text_file(file_name: str) -> str:
    """Reads the content of a text file and returns the file name if successful."""

    try:
        full_path = os.path.join(os.getcwd(), file_name)
        with open(full_path) as file:
            pass
    except UnicodeError:
        print(f'Error. App can use only text files.')
        exit()
    except FileNotFoundError as error:
        print(error)
        exit()
    return file_name


def validate_count(count: int) -> int:
    """Checking the value for type matching"""

    try:
        if not isinstance(count, int):
            raise ValueError('Error, need an integer number')
    except ValueError as error:
        print(error)
        exit()
    return count


def split_into_parts(string: str, count_symbol: int) -> Tuple[int, str, str, str]:
    """Splits the string into three parts."""

    length_line = len(string)
    start_part = string[:count_symbol]

    middle_start = length_line // 2 - count_symbol // 2
    middle_part = string[middle_start: middle_start + count_symbol]

    end_part = string[-count_symbol:]

    return length_line, start_part, middle_part, end_part


def main(file_name: str, count: int) -> List[str] | str:
    """Main controller."""

    with open(validate_text_file(file_name), encoding='utf-8') as file:
        line = file.read()
        length_line, start_part, middle_part, end_part = split_into_parts(line, validate_count(count))

    if length_line - count < 2:
        return [start_part, 'No middle symbol', end_part]
    elif length_line < count:
        return 'Your number of letters is greater than the file length'
    else:
        return [start_part, middle_part, end_part]


if __name__ == '__main__':
    filename = 'test_text.txt'
    count_char = 6
    result = main(filename, count_char)
    print(f'Chars input q-ty: {count_char}\n'
          f'{result}')
