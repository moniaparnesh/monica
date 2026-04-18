from django import forms
from django.apps import AppConfig
from .models import *
from .models import Category, product  # adjust if needed

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields ='__all__'

class sub_categoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields =['name', 'category']

class sub_sub_categoryForm(forms.ModelForm):
    class Meta:
        model=Subsubcategory
        fields=['name', 'subcategory']

class model_form(forms.ModelForm):
    class Meta:
        model=product
        fields='__all__'

class normal(forms.Form):
    product_name = forms.CharField(max_length=100)
    product_price = forms.IntegerField()
    product_quantity = forms.IntegerField()
    product_image = forms.ImageField()
    hair_type = forms.CharField(max_length=50, required=False)
    hair_color = forms.CharField(max_length=50, required=False)
    description = forms.CharField(max_length=200, required=False)
