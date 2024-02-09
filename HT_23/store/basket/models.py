from django.db import models
from django.core.validators import MinValueValidator

from product.models import Product
from users.models import User


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return round(sum(basket.sum() for basket in self), 2)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    objects = BasketQuerySet.as_manager()

    def sum(self):
        return round(float(self.product.discounted_price[1:]) * self.quantity, 2)

    def __str__(self):
        return self.product
