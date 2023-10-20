""" Користувачем вводиться початковий і кінцевий рік. Створити цикл, який виведе всі високосні роки
    в цьому проміжку (границі включно).
    P.S. Рік є високосним, якщо він кратний 4, але не кратний 100, а також якщо він кратний 400. """

star_year = int(input('Enter start year: '))
end_year = int(input('Enter end year: '))

for year in range(star_year, end_year + 1):
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        print(f'{year} is a leap year')
