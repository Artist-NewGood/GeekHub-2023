from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from .models import Basket
from .serializers import BasketSerializer


class BasketListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketSerializer

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


class BasketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)


class BasketClearView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        Basket.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def show_basket(request):

    if request.user.is_authenticated:
        items = Basket.objects.filter(user=request.user)
    else:
        items = ()

    context = {'title': 'Корзина',
               'items': items}
    return render(request, template_name='basket/basket.html', context=context)


@login_required
def basket_add(request, product_id):
    quantity = int(request.POST.get('quantity', 1))

    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(product=product, user=request.user)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=quantity)
    else:
        basket = baskets.first()
        basket.quantity += quantity
        basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_clear(request):
    Basket.objects.filter(user_id=request.user).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def change_basket_quantity(request, product_id):
    quantity = int(request.POST.get('quantity', 1))
    product = Product.objects.get(id=product_id)
    user = request.user

    basket_item, created = Basket.objects.get_or_create(product=product, user_id=user.id)
    basket_item.quantity = quantity
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
