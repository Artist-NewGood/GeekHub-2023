from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import UserFactory
from .factories import ProductFactory
from .factories import BasketFactory


class ChangeBasketQuantityAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.basket = BasketFactory(user=self.user, product=self.product, quantity=2)
        self.url = reverse('basket:change_basket_quantity', kwargs={'product_id': self.product.id})
        self.client.force_login(self.user)

    def test_change_basket_quantity(self):
        response = self.client.post(self.url, data={'quantity': 5})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_basket_item = self.user.basket_set.first()
        self.assertEqual(updated_basket_item.quantity, 5)
