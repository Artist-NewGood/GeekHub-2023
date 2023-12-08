from types import NoneType

from bs4 import BeautifulSoup
import re
from task_3.parsers.chrome_webstore.dataclasses import SitemapItem
from task_3.parsers.chrome_webstore.dataclasses import LocationItem
from task_3.parsers.chrome_webstore.dataclasses import LocationItemInfo


class ChromeWebstoreParser:
    BASE_URL = 'https://chrome.google.com'

    @staticmethod
    def parse_sitemap(response_text: str) -> list[SitemapItem]:
        soup = BeautifulSoup(response_text, 'lxml')

        return [
            SitemapItem(
                location=url.loc.text
            )
            for url in soup.select('sitemap')
        ]

    @staticmethod
    def parse_sitemap_url(response_text: str) -> list[LocationItem]:
        soup = BeautifulSoup(response_text, 'lxml')

        return [
            LocationItem(
                link=url.loc.text.strip('"'),
            )
            for url in soup.select('url')
        ]

    def parse_sitemap_url_item(self, response_text: str) -> LocationItemInfo:
        soup = BeautifulSoup(response_text, 'lxml')
        item_info = soup.find('div', class_='T4LgNb')
        return (
            LocationItemInfo(
                name=item_info.h1.text if len(item_info) > 0 else 'None',
                description=self.description(item_info),
                id=item_info.find('a').get('href').split('/', 2)[-1]

            )
        )

    @staticmethod
    def description(obj: BeautifulSoup) -> str:
        soup = obj.find('div', class_='uORbKe')
        p_tags = [p_tag.text if len(p_tag) > 0 else 'No description' for p_tag in soup.find_all('p')]
        total_description = ' '.join([re.sub(r'\n', '', p_tag) for p_tag in p_tags])

        return total_description
