from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import UserFactory
from .factories import ProductFactory
from .factories import BasketFactory


class RemoveFromBasketAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.product = ProductFactory()
        self.basket = BasketFactory(user=self.user, product=self.product, quantity=2)
        self.url = reverse('basket:basket_remove', kwargs={'basket_id': self.basket.id})
        self.client.force_login(self.user)

    def test_remove_from_basket(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user.basket_set.exists())
