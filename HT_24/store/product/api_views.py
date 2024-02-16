from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import SAFE_METHODS

from .serializers import ProductSerializer
from .serializers import CategorySerializer

from .models import Product
from .models import Category


class IsAdminUserOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAdminUserOrReadOnly]
    serializer_class = CategorySerializer
