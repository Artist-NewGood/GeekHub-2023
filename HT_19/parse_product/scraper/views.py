from subprocess import Popen

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from .models import Product
from .models import Basket
from .models import IdString


def index(request):
    return render(request, template_name='index.html', context={'title': 'Main'})


def add_product(request):
    return render(request, template_name='add_product.html', context={'title': 'Add product'})


def product_data(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request=request,
                  template_name='product.html',
                  context={'product': product})


def scraper_data(request):
    response = request.GET.get('id_string')
    IdString.objects.create(input_string=response)
    Popen(['python3', 'subscraper.py'])
    return redirect('scraper:add_product')


def show_all_products(request):
    return render(request, 'show_all_products.html', context={'products': Product.objects.all()})


def login(request):
    return render(request, template_name='login.html', context={'title': 'Login'})


def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(product=product)

    if not baskets.exists():
        Basket.objects.create(product=product, quantity=quantity)
    else:
        basket = baskets.first()
        basket.quantity += quantity
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def show_cart(request):
    cart_items = Basket.objects.all()
    return render(request, 'cart.html', {'cart_items': cart_items})


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_clear(request):
    Basket.objects.all().delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def change_basket_quantity(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    product = Product.objects.get(id=product_id)
    basket_item, created = Basket.objects.get_or_create(product=product)
    basket_item.quantity = quantity
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
