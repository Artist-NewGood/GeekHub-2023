from rest_framework import serializers

from .models import Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['id', 'user', 'product', 'quantity']
