from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ProductFactory
from .factories import UserFactory


class ProductAPITest(APITestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.admin_user = UserFactory(is_staff=True)

    def test_get_product_list(self):
        url = reverse('product:product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product:show_all_products')
        data = {
            'product_id': 'NewProductID',
            'brand_name': 'Test Brand',
            'product_name': 'Test Product',
            'category': 'Test Category',
            'discounted_price': '9.99',
            'price_before_discount': '19.99',
            'savings_percent': '50%',
            'product_link': 'http://example.com/test-product',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_detail(self):
        url = reverse('product:product-detail', kwargs={'pk': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


