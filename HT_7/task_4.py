""" Створіть функцію <morse_code>, яка приймає на вхід рядок у вигляді коду
    Морзе та виводить декодоване значення (латинськими літерами).
    Особливості:
        - використовуються лише крапки, тире і пробіли (.- )
        - один пробіл означає нову літеру
        - три пробіли означають нове слово
        - результат може бути case-insensitive (на ваш розсуд - великими чи маленькими літерами).
        - для простоти реалізації - цифри, знаки пунктуацїї, дужки, лапки тощо використовуватися не будуть.
          Лише латинські літери.
        - додайте можливість декодування сервісного сигналу SOS (...---...)

        Приклад:

        --. . . -.- .... ..- -...   .. ...   .... . .-. .

        результат: GEEKHUB IS HERE"""


def decode_morse(morse_code: str) -> None:
    """Morse to text decoding"""

    decode_table = {".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
                    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
                    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
                    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
                    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
                    "--..": "Z", "   ": " ", "...---...": "SOS"}

    word_split = map(lambda x: tuple(x.split()) + ('   ',), tuple(morse_code.split('   ')))

    try:
        decode_word = ''.join(decode_table[letter] for word in word_split for letter in word)
        print(f'Decode result: {decode_word}')
    except KeyError as err:
        print(f'Invalid morse code: {err}')


if __name__ == '__main__':
    decode_morse('--. . . -.- .... ..- -...   .. ...   .... . .-. .')
