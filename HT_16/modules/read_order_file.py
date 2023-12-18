import csv
from io import StringIO

import requests
from requests import HTTPError


class OrderRead:
    def __init__(self, link):
        self.__link = link

    def read_order_file(self) -> list[list[str]]:
        """Read data from the order file."""

        response = requests.get(self.__link)
        try:
            if response.status_code >= 400:
                raise HTTPError(f'Error. The server is unavailable. \nStatus code: {response.status_code} '
                                f'\nFor more information about status code use google.')
        except HTTPError as e:
            print(e)
            exit()

        csv_data = list(csv.reader(StringIO(response.text)))[1:]
        return csv_data
