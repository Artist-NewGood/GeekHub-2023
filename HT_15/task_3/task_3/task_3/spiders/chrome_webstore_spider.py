""" Використовуючи Scrapy, заходите на "https://chrome.google.com/webstore/sitemap",
    переходите на кожен лінк з тегів <loc>, з кожного лінка берете посилання на сторінки екстеншенів,
    парсите їх і зберігаєте в CSV файл ID, назву та короткий опис кожного екстеншена
    (пошукайте уважно де його можна взяти) """

import scrapy
from typing import Any
from urllib.parse import urljoin
from scrapy import Request
from scrapy.http import Response
from task_3.items import Task3Item
from task_3.parsers.chrome_webstore.parser import ChromeWebstoreParser


class ChromeWebstoreSpiderSpider(scrapy.Spider):
    parser = ChromeWebstoreParser()

    name = 'chrome_webstore_spider'
    start_urls = [urljoin(parser.BASE_URL, 'webstore/sitemap')]

    def parse(self, response: Response, **kwargs: Any):
        sitemap_results = self.parser.parse_sitemap(response.text)
        for result in sitemap_results:
            yield Request(
                url=result.location,
                callback=self.parse_location
            )

    def parse_location(self, response: Response):
        sitemap_url_result = self.parser.parse_sitemap_url(response.text)
        for url_result in sitemap_url_result:

            yield Request(
                url=url_result.link,
                callback=self.parse_location_info
            )

    def parse_location_info(self, response: Response):
        sitemap_url_item_result = self.parser.parse_sitemap_url_item(response.text)
        item = Task3Item(
               name=sitemap_url_item_result.name,
               description=sitemap_url_item_result.description,
               id=sitemap_url_item_result.id

        )
        yield item
