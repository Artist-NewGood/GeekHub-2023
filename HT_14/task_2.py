""" Створіть програму для отримання курсу валют за певний період.
    - отримати від користувача дату (це може бути як один день так і інтервал - початкова і кінцева дати,
      продумайте механізм реалізації) і назву валюти
    - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен день у вказаному інтервалі)
    - не забудьте перевірку на валідність введених даних"""

import requests
from datetime import datetime, timedelta
from prettytable import PrettyTable


class CurrencyRate:
    URL = 'https://api.privatbank.ua/p24api/exchange_rates?date='

    RULES = ('\nAttentions. Some rules\n'
             'The date is supported in the format DD.MM.YYYY (example 01.12.2020), where:\n'
             '- DD is the day (cannot be more than 31);\n'
             '- MM is the month (cannot be more than 12);\n'
             '- YYYY is the year (must be written in full and not more than the current year and\n'
             '!!! WARNING: The minimum date for which we can provide information is 01.12.2014')

    CURRENCY = ('USD', 'CHF', 'CZK', 'EUR', 'GBP', 'PLN', 'ILS', 'JPY', 'NOK')
    MIN_DATE = datetime(2014, 12, 1)
    MAX_DATE = datetime.now()

    def check_user_date(self, prompt: str) -> str:
        """Check the user's date for validity"""

        while True:
            try:
                user_date = datetime.strptime(input(prompt), '%d.%m.%Y')
            except ValueError:
                print('Error, need correct date format -> DD.MM.YYYY\n')
                continue

            if user_date > self.MAX_DATE:
                print('Error, you are not Klichko. Please, enter a real date)\n')
                continue
            elif user_date < self.MIN_DATE:
                print('Error, we do not support such a late date\n')
                continue

            return user_date.strftime('%d.%m.%Y')

    def check_user_currency(self, prompt: str) -> str:
        """Checks user currency for validity"""

        print('▼\n'
              'The currencies we work with are - USD, CHF, CZK, EUR, GBP, PLN, ILS, JPY, NOK')
        while True:

            user_currency = input(prompt)
            if user_currency not in self.CURRENCY:
                print(' ! Error, we do not support this currency. Try again\n')
                continue
            return user_currency

    def get_currency_rate_date(self) -> None:
        """Displays exchange rates in the form of a table for the selected date"""

        print(self.RULES)
        user_currency = False
        flag = 0

        if not self.choice_variant_currency():
            user_currency = self.check_user_currency('Enter your currency: ')

        user_date = self.check_user_date('Enter your date: ')

        response = requests.get(self.URL + user_date).json()

        table = PrettyTable()
        table.field_names = ['Currency', 'Sale rate', 'Purchase rate']

        for currency in response['exchangeRate']:
            if user_currency:
                if currency.get('purchaseRate', False) and currency.get('currency') == user_currency:
                    table.add_row([currency["currency"], currency["purchaseRate"], currency["saleRate"]])
                    flag = 1
            else:
                if currency.get('purchaseRate', False):
                    table.add_row([currency["currency"], currency["purchaseRate"], currency["saleRate"]])
                    flag = 1
        if not flag:
            print('\nSorry, as of this date, we have no information on this currency\n')
            self.back_menu()

        print(table)
        self.back_menu()

    def get_currency_rate_period_date(self) -> None:
        """Displays the exchange rate in the form of a table for each day of a certain period"""

        print(self.RULES)
        user_currency = False
        flag = 0

        if not self.choice_variant_currency():
            user_currency = self.check_user_currency('Enter your currency: ')

        date_start = datetime.strptime(self.check_user_date('Enter start date: '), '%d.%m.%Y').toordinal()
        while True:
            date_end = datetime.strptime(self.check_user_date('Enter end date: '), '%d.%m.%Y').toordinal()
            if date_end < date_start:
                print('Error, end date smaller start date\n')
                continue
            break

        table = PrettyTable()
        table.field_names = ['Currency', 'Sale rate', 'Purchase rate']

        for day in range(date_start, date_end + 1):
            response = requests.get(self.URL + datetime.fromordinal(day).strftime('%d.%m.%Y')).json()
            print(f'\n          Date: {datetime.fromordinal(day).strftime("%d.%m.%Y")}')

            for currency in response['exchangeRate']:
                if user_currency:
                    if currency.get('purchaseRate', False) and currency.get('currency') == user_currency:
                        table.add_row([currency["currency"], currency["purchaseRate"], currency["saleRate"]])
                        flag = 1
                else:
                    if currency.get('purchaseRate', False):
                        table.add_row([currency["currency"], currency["purchaseRate"], currency["saleRate"]])
                        flag = 1
            if not flag:
                print('\nSorry, as of this date, we have no information on this currency')
                continue
            print(table)
            table.clear_rows()

        self.back_menu()

    def back_menu(self) -> None:
        """Menu with additional options"""

        print('▼\n'
              '1. Back to main menu\n'
              '0. Exit')

        match input('Your choice: '):
            case '1':
                self.main()
            case '0':
                print('\n♥ Bye ♥')
                exit()
            case _:
                print(' ! Error number, try again\n')
                self.back_menu()

    def choice_variant_currency(self) -> bool:
        """Allows you to choose the option of information presentation"""

        print('\nMenu:\n'
              '1. Full list of currencies\n'
              '2. To choose from\n'
              '3. Back')

        while True:
            match input('\nYour choice: '):
                case '1':
                    return True
                case '2':
                    return False
                case '3':
                    self.main()
                case _:
                    print(' ! Error, need correct number (1, 2 or 3)')

    def main(self) -> None:
        """Main controller"""

        print('Welcome to our exchange.\n'
              'Here you can find out the exchange rate of the currency you need to UAH for a '
              'certain date or find out the exchange rate for a certain period.\n'
              'The currencies we work with are - USD, CHF, CZK, EUR, GBP, PLN, ILS, JPY, NOK')

        print('\nWhat you want:\n'
              '1. Currency rate for date\n'
              '2. Currency rate for period date\n'
              '\n'
              '0. Exit')

        while True:
            match input('\nYour choice: '):
                case '1':
                    self.get_currency_rate_date()
                case '2':
                    self.get_currency_rate_period_date()
                case '0':
                    print('\n♥ Bye ♥')
                    exit()
                case _:
                    print(' ! Error, need correct number (1, 2 or 0)')


if __name__ == '__main__':
    date = CurrencyRate()
    date.main()
