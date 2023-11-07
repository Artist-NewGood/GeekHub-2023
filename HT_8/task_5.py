""" Напишіть функцію,яка приймає на вхід рядок та повертає кількість окремих регістро-незалежних букв та цифр,
    які зустрічаються в рядку більше ніж 1 раз. Рядок буде складатися лише з цифр та букв (великих і малих).
    Реалізуйте обчислення за допомогою генератора.

    Example (input string -> result):
    "abcde" -> 0            # немає символів, що повторюються
    "aabbcde" -> 2          # 'a' та 'b'
    "aabBcde" -> 2          # 'a' присутнє двічі і 'b' двічі (`b` та `B`)
    "indivisibility" -> 1   # 'i' присутнє 6 разів
    "Indivisibilities" -> 2 # 'i' присутнє 7 разів та 's' двічі
    "aA11" -> 2             # 'a' і '1'
    "ABBA" -> 2             # 'A' і 'B' кожна двічі """


def count_unique_characters(text: str) -> int:
    """Finds the number of separate case-insensitive letters and digits, that occur more than 1 time in a string"""
    letter = tuple(char for char in set(text) if text.count(char) > 1)

    return len(letter)


if __name__ == '__main__':
    CASES = (
             ('abcde', 0),
             ('aabbcde', 2),
             ('aabBcde', 2),
             ('indivisibility', 1),
             ('Indivisibilities', 2),
             ('aA11', 2),
             ('ABBA', 2)
            )

    for case, answer in CASES:
        assert count_unique_characters(case.lower()) == answer
