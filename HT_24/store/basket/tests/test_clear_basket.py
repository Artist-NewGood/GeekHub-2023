from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import UserFactory
from .factories import ProductFactory
from .factories import BasketFactory


class ClearBasketAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product1 = ProductFactory()
        self.product2 = ProductFactory()
        self.basket1 = BasketFactory(user=self.user, product=self.product1, quantity=2)
        self.basket2 = BasketFactory(user=self.user, product=self.product2, quantity=1)
        self.url = reverse('basket:basket_clear')
        self.client.force_login(self.user)

    def test_clear_basket(self):
        self.assertEqual(self.user.basket_set.count(), 2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.basket_set.count(), 0)
