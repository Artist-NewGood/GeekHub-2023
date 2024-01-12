import django
django.setup()

from scraper.models import Product
from scraper.models import IdString
from scraper.sears_api import SearsProductParser


def extract_ids_from_string() -> str:
    """Extract and yield non-empty identifiers from the last record in the IdString model.
       This function retrieves the last string entry from IdString, replaces ';' and ',' with spaces,
       splits the string into individual elements, and yields each non-empty trimmed identifier."""

    string_object = IdString.objects.last()
    response = string_object.input_string

    if ';' in response:
        response.replace(';', ' ')
    if ',' in response:
        response.replace(',', ' ')

    response = response.split()

    for id_obj in response:
        if id_obj != '':
            yield id_obj.strip()


def main() -> None:
    """Main function to parse and update product information in the database.
       This function iterates over product IDs extracted from the last entry in the IdString model.
       It uses the SearsProductParser to parse each product's data and then updates or creates
       a corresponding Product instance in the database with the parsed information."""

    sears = SearsProductParser()
    for product_id in extract_ids_from_string():
        product = sears.parse_product_data(item_id=product_id)
        Product.objects.update_or_create(
            product_id=product_id,
            defaults={
                'product_id': product['product_id'],
                'brand_name': product['brand_name'],
                'product_name': product['product_name'],
                'category': product['category'],
                'discounted_price': product['discounted_price'],
                'price_before_discount': product['price_before_discount'],
                'savings_percent': product['savings_percent'],
                'product_link': product['product_link']
            }
        )


if __name__ == '__main__':
    main()
