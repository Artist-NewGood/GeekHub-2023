from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=15)
    brand_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,)
    discounted_price = models.CharField(max_length=10)
    price_before_discount = models.CharField(max_length=10)
    savings_percent = models.CharField(max_length=255)
    product_link = models.CharField(max_length=255)


class IdString(models.Model):
    input_string = models.CharField(max_length=1000)


class BaskerQuerySet(models.QuerySet):
    def total_sum(self):
        return round(sum(basket.sum() for basket in self), 2)


class Basket(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    objects = BaskerQuerySet.as_manager()

    def sum(self):
        return round(float(self.product.discounted_price[1:]) * self.quantity, 2)

