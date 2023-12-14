import requests
import csv
from io import StringIO


class OrderRead:
    def __init__(self, link):
        self.__link = link

    def read_order_file(self) -> list[list[str]]:
        """Read data from the order file."""

        response = requests.get(self.__link).text
        csv_data = list(csv.reader(StringIO(response)))[1:]
        return csv_data
