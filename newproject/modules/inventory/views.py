from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from modules.inventory.models import Product, Category, Company, Tag
from modules.inventory.forms import ProductForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

# Create your views here.
class ProductCreateView(CreateView):
	form_class = ProductForm
	template_name = 'product/create.html'

	def form_valid(self, form):
		data = form.save(commit=False)
		data.user = self.request.user
		category = self.request.POST['category']
		category = Category.objects.filter(name=category)
		if category:
			data.category = category[0]
		# else:
		# 	Category.objects.create(name=category)
		# 	category = Category.objects.filter(name=category)
		# 	data.category = category[0]
		company = self.request.POST['company']
		company = Company.objects.filter(name=company)
		if company:
			data.company = company[0]
		data.save()
		tags = self.request.POST['tags']
		tags = tags.split(',')
		for tag in tags:
			tags = Tag.objects.filter(name=tag)
			if tags:
				data.tags.add(tags[0])
			else:
				data.tags.create(name=tag)		
		return redirect('inventory:product_list')

class ProductListView(ListView):
	model = Product
	template_name = 'product/list.html'
	context_object_name = 'product_list'

class ProductDetailView(DetailView):
	model = Product
	template_name = 'product/detail.html'
	context_object_name = 'product'

class ProductUpdateView(UpdateView):
	model = Product
	form_class = ProductForm
	template_name = 'product/update.html'
	pk_url_kwarg = 'pk'

	def form_valid(self, form):
		data = form.save(commit=False)
		data.user = self.request.user
		category = self.request.POST['category']
		category = Category.objects.filter(name=category)
		if category:
			data.category = category[0]
		company = self.request.POST['company']
		company = Company.objects.filter(name=company)
		if company:
			data.company = company[0]
		data.save()
		tags = self.request.POST['tags']
		tags = tags.split(',')
		for tag in tags:
			tags = Tag.objects.filter(name=tag)
			if tags in data.tags.all():
				continue
			else:
				if tags:
					data.tags.add(tags[0])
				else:
					data.tags.create(name=tag)		
		return redirect('inventory:product_list')

class ProductDeleteView(DeleteView):
	model = Product
	template_name = 'product/delete.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('inventory:product_list')



	