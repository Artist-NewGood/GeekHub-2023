""" Напишіть функцію,яка прймає рядок з декількох слів і повертає довжину найкоротшого слова.
    Реалізуйте обчислення за допомогою генератора. """


def shortest_word_length(text: str) -> int:
    """Takes a string of several words and returns the length of the shortest word."""
    len_word = min(len(word) for word in text.split())
    # min_len_word = min(text.split(), key=len)

    return len_word


if __name__ == '__main__':
    some_text = input('Enter please some text: ')
    result = shortest_word_length(some_text)
    print(f'Length shortest word: {result}')
