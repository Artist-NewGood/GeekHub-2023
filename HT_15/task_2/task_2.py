""" Викорисовуючи requests, заходите на ось цей сайт "https://www.expireddomains.net/deleted-domains/"
    (з ним будьте обережні), вибираєте будь-яку на ваш вибір доменну зону і парсите список  доменів - їх там буде
    десятки тисяч (звичайно ураховуючи пагінацію). Всі отримані значення зберігти в CSV файл. """

import requests
import csv
import random
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
<<<<<<< HEAD
from dataclasses import fields
=======
from dataclasses import fields, astuple
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653
from dataclasses import dataclass


@dataclass
class DomainRow:
    domain: str
    bl: str
    domainpop: str
    abirth: str
    aentries: str
    dmoz: str
    statuscom: str
    statusnet: str
    statusorg: str
    statusde: str
    statustld_registered: str
    related_cnobi: str
    enddate: str


<<<<<<< HEAD
class ExpiredDomainsParser:
=======
class Parse:
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653
    RESULT_CSV = 'domain.csv'
    DOMAIN_ROW = [field.name for field in fields(DomainRow)]
    MAIN_URL = 'https://www.expireddomains.net'
    PAGE_URL = '/expired-domains/'
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                  "*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.expireddomains.net/expired-domains/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "X-Amzn-Trace-Id": "Root=1-6571bae8-18ec31306354ea3c30934a5b"
    }

<<<<<<< HEAD
    def fetch_and_parse_domain_data(self) -> None:
        """ Initiates the web crawling process to extract domain information from the specified URL"""
=======
    def parser(self) -> None:
        """Main controller"""
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653

        info = []
        print('Parsing')
        while True:
<<<<<<< HEAD
=======
            sleep(random.choice(range(7, 20)))
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653

            response = requests.get(urljoin(self.MAIN_URL, self.PAGE_URL), headers=self.HEADERS)
            soup = BeautifulSoup(response.text, 'lxml')

            fields_info = soup.find('tbody')
            if not fields_info:
                break
<<<<<<< HEAD
            domain_info = [self.parse_single_domain_data(info) for info in fields_info.find_all('tr')]

            next_page = soup.find('a', class_='next')

            info.extend(domain_info)
            self.write_to_csv(info)
            sleep(random.choice(range(7, 20)))
=======
            domain_info = [self.parse_single_domain(info) for info in fields_info.find_all('tr')]

            next_page = soup.find('a', class_='next')
            info.extend(domain_info)
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653

            if next_page:
                self.PAGE_URL = next_page['href']
                print('Steel parsing...')
            else:
                break
<<<<<<< HEAD
        print('\nEND')

    @staticmethod
    def parse_single_domain_data(odj: BeautifulSoup) -> tuple:
=======
        self.write_to_csv(info)

    @staticmethod
    def parse_single_domain(odj: BeautifulSoup) -> tuple:
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653
        """Parse text from every data of domain"""

        domain = odj.select_one('.field_domain').text
        bl = odj.select_one('.field_bl').select_one('a')['title'][0]
        domainpop = odj.select_one('.field_domainpop').text
        abirth = odj.select_one('.field_abirth').text
        aentries = odj.select_one('.field_aentries').text
        dmoz = odj.select_one('.field_dmoz').text
        statuscom = odj.select_one('.field_statuscom').text
        statusnet = odj.select_one('.field_statusnet').text
        statusorg = odj.select_one('.field_statusorg').text
        statusde = odj.select_one('.field_statusde').text
        statustld_registered = odj.select_one('.field_statustld_registered').text
        related_cnobi = odj.select_one('.field_related_cnobi').text
        enddate = odj.select_one('.field_enddate').text

        return (domain, bl, domainpop, abirth, aentries, dmoz, statuscom, statusnet, statusorg, statusde,
                statustld_registered, related_cnobi, enddate)

    def write_to_csv(self, domain_info) -> None:
        """Writes the selected product data to a csv file"""

        with open(self.RESULT_CSV, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)

            csv_writer.writerow(self.DOMAIN_ROW)
            csv_writer.writerows(domain_info)

<<<<<<< HEAD

if __name__ == '__main__':
    p = ExpiredDomainsParser()
    p.fetch_and_parse_domain_data()
=======
            print('\nEND')


if __name__ == '__main__':
    p = Parse()
    p.parser()
>>>>>>> 7418385abad29a5e9aa0f5db0089d8fa42451653
