from rest_framework import serializers

from .models import Product
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'brand_name', 'product_name', 'category', 'discounted_price',
                  'price_before_discount', 'savings_percent', 'product_link']
