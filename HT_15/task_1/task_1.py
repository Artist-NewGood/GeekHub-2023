""" Викорисовуючи requests, написати скрипт, який буде приймати на вхід ID категорії із сайту https://www.sears.com
    і буде збирати всі товари із цієї категорії, збирати по ним всі можливі дані
    (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл (наприклад, якщо категорія має ID 12345,
    то файл буде називатись 12345_products.csv)

    Наприклад, категорія https://www.sears.com/tools-tool-storage/b-1025184 має ІД 1025184"""

import csv
import requests
from datetime import datetime
from random import choice
from time import sleep


class Parse:

    ORIGINAL_URL = 'https://www.sears.com'

    HEADERS = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'uk,ru;q=0.9',
        'authorization': 'SEARS',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    ID_CATEGORY = input('Enter id category: ')
    CSV_FILE = 'products_info.csv'

    CSV_FIELDS = ['Brand_name', 'Product_name', 'Discounted_price',
                  'Price_before_discount', '~Savings percent', 'Savings money', 'Product link']

    def parsing(self) -> None:
        """Makes a request to the API and receives a JSON file with product data for a given category id"""

        print('Start:', datetime.now())

        start_index = 1
        end_index = 48
        products_info = []

        while True:
            print(f'Parse products from {start_index} to {end_index}')
            sleep(choice(range(7, 15)))

            request_url = (f'https://www.sears.com/api/sal/v3/products/search?startIndex='
                           f'{start_index}&endIndex={end_index}&searchType=category&catalogId='
                           f'12605&store=Sears&storeId=10153&zipCode=10101&bratRedirectInd='
                           f'true&catPredictionInd=true&disableBundleInd=true&filterValueLimit='
                           f'500&includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection='
                           f'true&sortBy=ORIGINAL_SORT_ORDER&whiteListCacheLoad=false&eagerCacheLoad='
                           f'true&slimResponseInd=true&catGroupId=')

            response = requests.get(request_url + self.ID_CATEGORY, headers=self.HEADERS).json()

            try:
                for item in response['items']:
                    if len(item['price']['finalPriceDisplay'].split('-')) == 2:
                        savings_percent, savings_money = self.calculate_savings(item['price']['finalPriceDisplay'],
                                                                                item['price']['regularPriceDisplay'], )

                    elif not item['price'].get('savingsDisplay', False):
                        savings_percent = 'No savings'
                        savings_money = 0 if not item['price']['messageTags']['savings'] \
                            else item['price']['messageTags']['savings']
                    else:
                        savings_percent = item['price']['savingsDisplay']
                        savings_money = item['price']['messageTags']['savings']

                    products_info.append((item['brandName'], item['name'], item['price']['finalPriceDisplay'],
                                          item['price']['regularPriceDisplay'],savings_percent, savings_money,
                                          self.ORIGINAL_URL + item['additionalAttributes']['seoUrl']))
                start_index += 48
                end_index += 48
                sleep(choice(range(7, 15)))
            except KeyError:
                break

        self.write_to_csv(products_info)

    @staticmethod
    def calculate_savings(price: str, reg_price: str) -> tuple[str, str]:
        """Calculate percent and savings for special product"""

        avg_final_price_display = sum(
            [float(price.strip('$ ').replace(',', '')) for price in price.split('-')]) / 2

        avg_regular_price_display = sum(
            [float(price.strip('$ ').replace(',', '')) for price in reg_price.split('-')]) / 2

        savings_percent = int(((avg_regular_price_display - avg_final_price_display) / avg_regular_price_display) * 100)
        savings_money = avg_regular_price_display - avg_final_price_display
        return str(savings_percent) + '%', '$' + str(savings_money)

    def write_to_csv(self, authors_info: list) -> None:
        """Writes the selected product data to a csv file"""

        with open(self.CSV_FILE, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(self.CSV_FIELDS)
            csv_writer.writerows(authors_info)

            print('End:', datetime.now())


if __name__ == '__main__':
    p = Parse()
    p.parsing()
