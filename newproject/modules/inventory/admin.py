from django.contrib import admin
from modules.inventory.models import Product, Category, Company

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Company)