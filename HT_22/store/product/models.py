from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.CharField(max_length=15)
    brand_name = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    discounted_price = models.CharField(max_length=10)
    price_before_discount = models.CharField(max_length=10)
    savings_percent = models.CharField(max_length=255)
    product_link = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name


class IdString(models.Model):
    input_string = models.CharField(max_length=1000)

    def __str__(self):
        return self.input_string
