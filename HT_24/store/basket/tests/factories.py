import factory

from basket.models import Basket
from users.models import User
from product.models import Product
from product.models import Category

TEST_PASSWORD = 'password12345'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'Category %d' % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    product_id = factory.Sequence(lambda n: 'product%d' % n)
    brand_name = factory.Faker('company')
    product_name = factory.Sequence(lambda n: 'Product %d' % n)
    category = factory.SubFactory(CategoryFactory)
    discounted_price = factory.Faker('random_number', digits=2)
    price_before_discount = factory.Faker('random_number', digits=2)
    savings_percent = factory.Faker('random_number', digits=2)
    product_link = factory.Faker('url')


class BasketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Basket

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1
