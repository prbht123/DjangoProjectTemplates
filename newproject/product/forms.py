from django import forms
from product.models import Product, Address, Stock, Customer

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name','price','manufacturing_date','expiry_date','image','description']

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = "__all__"

class StockForm(forms.ModelForm):
	class Meta:
		model = Stock
		fields = ['product','quantity','image']

class CustomerForm(forms.ModelForm):
	class Meta:
		model = Customer
		exclude = ['created_at','updated_at']