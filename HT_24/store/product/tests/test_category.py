from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import CategoryFactory
from .factories import UserFactory


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.category = CategoryFactory()
        self.admin_user = UserFactory(is_staff=True)

    def test_get_category_list(self):
        url = reverse('product:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product:category-list')
        data = {
            'name': 'Test Category',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_category_detail(self):
        url = reverse('product:category-detail', kwargs={'pk': self.category.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('product:category-detail', kwargs={'pk': self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

