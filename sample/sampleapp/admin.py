from django.contrib import admin
from .models import *
admin.site.register(signup)
admin.site.register(product)
admin.site.register(cart)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Subsubcategory)
admin.site.register(delivery_boy_register)