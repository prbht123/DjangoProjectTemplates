from django import forms
from modules.inventory.models import Product

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = ['name','image','company','category','price','manufacturing_date','expiry_date','quantity','description']