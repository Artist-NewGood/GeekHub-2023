""" Написати функцiю season, яка приймає один аргумент (номер мiсяця вiд 1 до 12) та яка буде
    повертати пору року, якiй цей мiсяць належить (зима, весна, лiто або осiнь).
    У випадку некоректного введеного значення - виводити відповідне повідомлення. """


def season(month):
    seasons = {'Winter': (12, 1, 2), 'Spring': (3, 4, 5),
               'Summer': (6, 7, 8), 'Autumn': (9, 10, 11)}

    for key, val in seasons.items():
        if month in val:
            return key


def check_number_of_month(prompt):
    while True:
        try:
            month = int(input(prompt))
            if month not in range(1, 13):
                raise IndexError
            return month
        except ValueError:
            print('Error. Incorrect input data. Please, enter a correct NUMBER of month (1-12)\n')
        except IndexError:
            print('Error. Incorrect number of month. Please, enter a correct number of month (1-12)\n')


if __name__ == "__main__":
    number_of_month = check_number_of_month('Please, enter a number of month: ')
    print(f'Season of year: {season(number_of_month)}')