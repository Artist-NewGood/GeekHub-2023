from random import choice
from time import sleep
from typing import Any
from urllib.parse import urljoin

import requests


class SearsProductParser:
    ORIGINAL_URL = 'https://www.sears.com'
    HEADERS = {
        'authority': 'www.sears.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'authorization': 'SEARS',
        'content-type': 'application/json',
        'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }

    def parse_product_data(self, item_id: Any):
        """Makes requests to the API to retrieve product data for the specified product ID.
        This function retrieves information such as product ID, brand, name, category, discounted price,
        price before discount, discount amount, and a link to the product. The received information is
        returned in the form of a dictionary to the call point of the function."""

        sleep(choice(range(4, 7)))
        request_url = (f'https://www.sears.com/api/sal/v3/products/search?q={item_id}&startIndex=1&endIndex=48&'
                       f'searchType=keyword&catalogId=12605&store=Sears&storeId=10153&zipCode=10101&'
                       f'bratRedirectInd=true&catPredictionInd=true&disableBundleInd=true&filterValueLimit=500&'
                       f'includeFiltersInd=true&shipOrDelivery=true&solrxcatRedirection=true&sortBy=ORIGINAL_SORT_ORDER&'
                       f'whiteListCacheLoad=false&eagerCacheLoad=true&slimResponseInd=true&catRecommendationInd=true')

        response = requests.get(request_url, headers=self.HEADERS).json()['items'][0]

        if len(response['price']['finalPriceDisplay'].split('-')) == 2:
            savings_percent, avg_final_price_display = (
                self.calculate_savings(response['price']['finalPriceDisplay'],
                                       response['price']['regularPriceDisplay'], ))

        elif not response['price'].get('savingsDisplay', False):
            savings_percent = 'No savings'
            avg_final_price_display = response['price']['finalPriceDisplay']

        else:
            savings_percent = response['price']['savingsDisplay']
            avg_final_price_display = response['price']['finalPriceDisplay']

        return dict(
            product_id=response['partNum'],
            brand_name=response['brandName'],
            product_name=response['name'],
            category=response['category'],
            discounted_price=avg_final_price_display.replace(',', ''),
            price_before_discount=response['price']['regularPriceDisplay'].replace(',', ''),
            savings_percent=savings_percent,
            product_link=urljoin(self.ORIGINAL_URL, response['additionalAttributes']['seoUrl'])
        )

    @staticmethod
    def calculate_savings(price: str, reg_price: str) -> tuple[str, str]:
        """Calculate percent and savings for special product"""

        avg_final_price_display = sum(
            [float(price.strip('$ ').replace(',', '')) for price in price.split('-')]) / 2

        avg_regular_price_display = sum(
            [float(price.strip('$ ').replace(',', '')) for price in reg_price.split('-')])

        savings_percent = int(((avg_regular_price_display - avg_final_price_display) / avg_regular_price_display) * 100)

        return str(savings_percent) + '%',  '$' + str(avg_final_price_display)
