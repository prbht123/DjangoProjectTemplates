from django.contrib import admin
from product.models import Product, Category, Tag, Company, Address, Stock, Customer, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(Stock)
admin.site.register(Customer)
admin.site.register(Cart)
