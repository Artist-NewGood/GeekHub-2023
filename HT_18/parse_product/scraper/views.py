from subprocess import Popen

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template import loader

from .models import Product
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


def cart(request):
    return render(request, template_name='cart.html', context={'title': 'Cart'})


def login(request):
    return render(request, template_name='login.html', context={'title': 'Login'})
