""" Створiть 3 рiзних функцiї (на ваш вибiр). Кожна з цих функцiй повинна повертати якийсь результат
    (напр. інпут від юзера, результат математичної операції тощо). Також створiть четверту ф-цiю,
    яка всередині викликає 3 попереднi, обробляє їх результат та також повертає результат своєї роботи.
    Таким чином ми будемо викликати одну (четверту) функцiю, а вона в своєму тiлi - ще 3. """


def digits(input_string):
    numbers = set(digit for digit in input_string if digit in '0123456789')
    return numbers


def consonant_letters(input_string):
    con_letter = 'BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz'
    con_letters = set(letter for letter in input_string if letter in con_letter)
    return con_letters


def vowel_letters(input_string):
    vow_letters = set(letter for letter in input_string if letter in 'aeiouyAEIOUY')
    return vow_letters


def main_string(input_string):
    sort_digit = ' '.join(sorted(digits(input_string)))
    sort_consonant_letters = ' '.join(sorted(consonant_letters(input_string)))
    sort_vowel_letters = ' '.join(sorted(vowel_letters(input_string)))

    return f'\nDigits used in the string: {sort_digit}\n' \
           f'Consonant letters used in a string: {sort_consonant_letters}\n' \
           f'Vowels letters used in a string: {sort_vowel_letters}'


if __name__ == "__main__":
    user_input = input('Enter some string: ')
    result = main_string(user_input)
    print(result)