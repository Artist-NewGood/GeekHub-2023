from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import UserFactory
from .factories import ProductFactory


class AddToBasketAPITest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user.save()

        self.product = ProductFactory()
        self.url = reverse('basket:add_basket', kwargs={'product_id': self.product.id})
        self.client.force_login(self.user)

    def test_add_to_basket(self):
        self.assertEqual(self.user.basket_set.count(), 0)
        response = self.client.post(self.url, data={'quantity': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.basket_set.count(), 1)

        new_basket_item = self.user.basket_set.first()
        self.assertEqual(new_basket_item.product, self.product)
        self.assertEqual(new_basket_item.quantity, 2)
