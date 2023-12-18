import csv
from io import StringIO

import requests
from requests import HTTPError


class OrderRead:
    def __init__(self, link):
        self.__link = link

    def read_order_file(self) -> list[list[str]]:
        """Read data from the order file."""

        try:
            response = requests.get(self.__link)
            response.raise_for_status()
        except HTTPError as err:
            print(err)
            exit()

        csv_data = list(csv.reader(StringIO(response.text)))[1:]
        return csv_data
