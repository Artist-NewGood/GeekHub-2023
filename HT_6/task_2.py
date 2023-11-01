""" Написати функцію <bank> , яка працює за наступною логікою: користувач робить вклад у розмірі <a> одиниць
    строком на <years> років під <percents> відсотків (кожен рік сума вкладу збільшується на цей відсоток,
    ці гроші додаються до суми вкладу і в наступному році на них також нараховуються відсотки).
    Параметр <percents> є необов'язковим і має значення по замовчуванню <10> (10%).
    Функція повинна принтануть суму, яка буде на рахунку, а також її повернути (але округлену до копійок). """


def bank(money, years, percents=10):
    start_amount = money
    for i in range(years):
        money += money / percents

    print(f'\nThe amount that will be returned:\n'
          f'Your start money: {start_amount}$\n'
          f'Your percent per {years} years: {round(money - start_amount, 2)}$\n'
          f'Final result: {round(money, 2)}$')
    return round(money, 2)


def validation_number(number: str) -> int:
    try:
        return int(number)
    except ValueError:
        print('Error, need some an integer number')
        exit()


if __name__ == '__main__':
    deposit_amount = validation_number(input('Please enter the amount of your deposit: '))
    period = validation_number(input('For what period do you want to put it in? (minimum 1 year): '))
    result = bank(deposit_amount, period)
