from subprocess import Popen

from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect


from .models import Product, Category
from .models import IdString
from .forms import EditProductForm
from .services.utils import checking_access_rights


def index(request):
    context = {
        'title': 'Головна'
    }
    return render(request, 'product/index.html', context=context)


def add_product(request):
    if checking_access_rights(request):
        return redirect('/')
    context = {
        'title': 'Додати продукт'
    }
    return render(request, 'product/add_product.html', context=context)


def show_all_products(request, category_name=None, page_number=1):

    if category_name:
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category).order_by('id')
    else:
        products = Product.objects.all().order_by('id')

    per_page = 10
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {'title': 'Каталог',
               'products': products_paginator,
               'categories': Category.objects.all()
               }
    return render(request, template_name='product/show_all_products.html', context=context)


def scraper_product(request):
    response = request.GET.get('id_string')
    IdString.objects.create(input_string=response)
    Popen(['python3', 'product/services/subscraper.py'])
    return redirect('product:add_product')


def product_detail(request, product_id):
    context = {'title': 'Детальна інформація про продукт',
               'product_detail': Product.objects.get(id=product_id)
               }

    return render(request, template_name='product/product_detail.html', context=context)


def del_products(request, product_id):
    if checking_access_rights(request):
        return redirect('/')
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect(to='product:show_all_products')


def edit_product(request, product_id):
    if checking_access_rights(request):
        return redirect('/')

    context = {'product_detail': Product.objects.get(id=product_id),

               'categories': Category.objects.all()}

    return render(request, template_name='product/edit_product.html', context=context)


def save_edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product:product_detail', product_id=product.id)
        else:
            print(form.errors)
    else:
        form = EditProductForm(instance=product)

    context = {'form': form}
    return render(request, 'product/edit_product.html', context=context)
