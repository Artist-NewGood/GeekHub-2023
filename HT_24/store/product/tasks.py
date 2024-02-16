from celery import shared_task

from product.models import Product
from product.models import Category
from product.models import IdString

from product.services.sears_product_parser import SearsProductParser


@shared_task(name='start_scraping_task', queue='celery')
def start_scraping_task():
    """Extract and yield non-empty identifiers from the last record in the IdString model.
       This function retrieves the last string entry from IdString, replaces ';' and ',' with spaces,
       splits the string into individual elements"""

    string_object = IdString.objects.last()
    response = string_object.input_string

    if ';' in response:
        response.replace(';', ' ')
    if ',' in response:
        response.replace(',', ' ')

    response = response.split()

    sears = SearsProductParser()
    for product_id in response:
        product = sears.parse_product_data(item_id=product_id)
        category_name = product['category'].split('_')[-1]
        category, _ = Category.objects.get_or_create(name=category_name)

        Product.objects.update_or_create(
            product_id=product_id,
            defaults={
                'product_id': product['product_id'],
                'brand_name': product['brand_name'],
                'product_name': product['product_name'],
                'category': category,
                'discounted_price': product['discounted_price'],
                'price_before_discount': product['price_before_discount'],
                'savings_percent': product['savings_percent'],
                'product_link': product['product_link']
            }
        )
