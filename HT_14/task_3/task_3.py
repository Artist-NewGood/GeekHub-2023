""" http://quotes.toscrape.com/ - написати скрейпер для збору всієї доступної інформації про записи:
    цитата, автор, інфа про автора тощо.

    - збирається інформація з 10 сторінок сайту.
    - зберігати зібрані дані у CSV файл """


import csv
import requests
from bs4 import BeautifulSoup


class QuotesScraper:
    ORIGINAL_URL = 'https://quotes.toscrape.com/'
    RESULT_CSV = 'quotes.csv'
    page_url = 'https://quotes.toscrape.com/'

    def parse_quotes(self) -> None:
        """A general parser algorithm that collects all the necessary information about each author"""

        authors_info = []
        while True:

            response = requests.get(self.page_url)

            soup = BeautifulSoup(response.text, 'lxml')
            quotes = soup.find_all(class_='quote')

            info = [self.parse_single_quotes(quote) for quote in quotes]

            next_page = soup.find('li', class_='next')
            authors_info.extend(info)

            if next_page:
                self.page_url = self.ORIGINAL_URL + next_page.find('a')['href']
            else:
                break

        self.write_to_csv(authors_info)

    def parse_single_quotes(self, obj: BeautifulSoup) -> tuple[str, str, str, str, str, str]:
        """Parses information in the form of the author, his/her quote and tags"""

        quote = obj.select_one('.text').text
        author = obj.select_one('.author').text
        tag = obj.select_one('.keywords').get('content')

        born_date, born_place, description = self.parse_about_author((obj.select_one('a')['href']))

        return quote, author, born_place, born_date, tag, description

    def parse_about_author(self, link: str) -> tuple[str, str, str]:
        """Parses information about the author in the form of month of birth and date of birth"""

        about_author_link = self.ORIGINAL_URL + link

        response_1 = requests.get(about_author_link)
        soup = BeautifulSoup(response_1.text, 'lxml')

        author_born_date = soup.select_one('.author-born-date').text
        author_born_location = soup.select_one('.author-born-location').text.replace('in ', '')
        author_description = soup.select_one('.author-description').text.strip()

        return author_born_date, author_born_location, author_description

    def write_to_csv(self, authors_info: list) -> None:

        with open(self.RESULT_CSV, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')

            csv_writer.writerow(['quote', 'author', 'author_born_place', 'author_born_date', 'tags', 'description'])
            csv_writer.writerows(authors_info)


if __name__ == '__main__':
    data = QuotesScraper()
    data.parse_quotes()
