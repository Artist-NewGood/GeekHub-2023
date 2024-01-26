from django import forms

from .models import Product


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_id', 'brand_name', 'product_name', 'category', 'discounted_price',
                  'price_before_discount', 'savings_percent', 'product_link')
