from django.shortcuts import render, redirect
from product.models import Product, Category, Tag, Company, Customer, Address, Stock, Cart
from blog.models import Post
from product.forms import ProductForm, CustomerForm, AddressForm, StockForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin


# Create your views here.

class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class productCreate(SuperuserRequiredMixin, CreateView):
	form_class = ProductForm
	template_name = 'product/create.html'
	extra_context = {'companies':Company.objects.all(),'categories':Category.objects.all(),'tags':Tag.objects.all()}

	def form_valid(self, form):
		product = form.save(commit=False)
		product.author = self.request.user
		company = self.request.POST.get('company1', None)
		if company:
			company_name = Company.objects.filter(name=company)
			product.company = company_name[0]
		else:
			company = self.request.POST['company2']
			if company in Company.objects.all():
				company_name = Company.objects.filter(name=company)
				product.company = company_name[0]
			if company not in Company.objects.all():
				company_name = Company.objects.create(name=company)				
				product.company = company_name
		category = self.request.POST.get('category1', None)
		if category:
			category_value = Category.objects.filter(name=category)
			product.category = category_value[0]
		else:
			category = self.request.POST['category2']
			if category in Category.objects.all():
				category_value = Category.objects.filter(name=category)
				product.category = category_value[0]
			if category not in Category.objects.all():
				category_value = Category.objects.create(name=category)
				product.category = category_value 
		product.save()
		tag = self.request.POST['tag']
		tags = tag.split(',')
		if '' in tags:
			tags.remove('')
		for tag in tags:
			tag_value = Tag.objects.filter(name=tag)
			if tag_value:
				product.tags.add(tag_value[0])
			else:
				product.tags.create(tag)
		return redirect('product:product_list')

class productList(ListView):
	model = Product
	template_name = 'product/list.html'
	context_object_name = 'product_list'

class detailProduct(DetailView):
	model = Product
	template_name = 'product/detail.html'
	context_object_name = 'product'


class updateProduct(SuperuserRequiredMixin, UpdateView):
	model = Product
	form_class = ProductForm
	template_name = 'product/update.html'
	success_url = reverse_lazy('product:product_list')
	extra_context = {'companies':Company.objects.all(), 'categories':Category.objects.all(), 'tags':Tag.objects.all()}

	def form_valid(self, form):
		product = form.save(commit=False)
		product.author = self.request.user
		company = self.request.POST['company2']
		if company:
			if company in Company.objects.all():
				company_name = Company.objects.filter(name=company)
				product.company = company_name[0]
			if company not in Company.objects.all():
				company_name = Company.objects.create(name=company)
				product.company = company_name	
		else:
			company = self.request.POST.get('company1', None)
			company_name = Company.objects.filter(name=company)
			if company_name:
				product.company = company_name[0]				
		category = self.request.POST['category2']
		if category:
			if category in Category.objects.all():
				category_value = Category.objects.filter(name=category)
				product.category = category_value[0]
			if category not in Category.objects.all():
				category_value = Category.objects.create(name=category)
				product.category = category_value
		else:
			category = self.request.POST.get('category1', None)
			category_value = Category.objects.filter(name=category)
			product.category = category_value[0]
		product.save()
		tag = self.request.POST['tag']
		tags = tag.split(',')
		if '' in tags:
			tags.remove('')
		for item in product.tags.all():
			if item not in tags:
				product.tags.remove(item)	
		for tag in tags:
			tag_value = Tag.objects.filter(name=tag)															
			if tag_value in product.tags.all():
				continue
			else:
				if tag_value:
					product.tags.add(tag_value[0])
				else:
					product.tags.create(name=tag)	
		return redirect('product:product_list')


class deleteProduct(SuperuserRequiredMixin, DeleteView):
	model = Product
	template_name = 'product/delete.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('product:product_list')

class createStock(CreateView):
	form_class = StockForm
	template_name = 'stock/create.html'
	extra_context = {'companies':Company.objects.all()}

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['AddressForm'] = AddressForm()
		return context

	def form_valid(self,form):
		address = AddressForm(self.request.POST)
		if address.is_valid():
			address_data = address.save()
			stock = form.save(commit=False)
			stock.address = address_data
			stock.owner = self.request.user
			company = self.request.POST.get('company1', None)
			if company:
				company_name = Company.objects.filter(name=company)
				stock.company = company_name[0]
			else:
				company = self.request.POST['company2']
				if company in Company.objects.all():
					company_name = Company.objects.filter(name=company)
					stock.company = company_name[0]
				if company not in Company.objects.all():
					company_name = Company.objects.create(name=company)				
					stock.company = company_name
			stock.save()
			return redirect('product:stock_list')

class listStock(ListView):
	model = Stock
	template_name = 'stock/list.html'
	context_object_name = 'stock_list'


class detailStock(DetailView):
	model = Stock
	template_name = 'stock/detail.html'
	success_url = reverse_lazy('product:stock_list')
	context_object_name = 'stock'

class updateStock(UpdateView):
	model = Stock
	form_class = StockForm
	template_name = 'stock/update.html'
	extra_context = {'companies':Company.objects.all()}

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['AddressForm'] = AddressForm(instance=self.get_object().address)
		return context

	def form_valid(self, form):
		stock = form.save(commit=False)
		address = AddressForm(self.request.POST, instance=self.get_object().address)
		if address.is_valid():
			address_data = address.save()
			stock.address = address_data
		stock.owner = self.request.user
		company = self.request.POST['company2']
		if company:
			if company in Company.objects.all():
				company_name = Company.objects.filter(name=company)
				stock.company = company_name[0]
			if company not in Company.objects.all():
				company_name = Company.objects.create(name=company)
				stock.company = company_name	
		else:
			company = self.request.POST.get('company1', None)
			company_name = Company.objects.filter(name=company)
			stock.company = company_name[0]
		stock.save()
		return redirect('product:stock_list')

class deleteStock(DeleteView):
	model = Stock
	template_name = 'stock/delete.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('product:stock_list')

def CreateStock(request):
	stock_form = StockForm(request.POST or None, request.FILES or None)
	address_form = AddressForm(request.POST or None)
	companies = Company.objects.all()

	if request.method == 'POST':
		if stock_form.is_valid():
			stock = stock_form.save(commit=False)
			if address_form.is_valid():
				address_data = address_form.save()
				stock.address = address_data
			stock.owner = request.user
			company = request.POST.get('company1', None)
			if company:
				company_name = Company.objects.filter(name=company)
				stock.company = company_name[0]
			else:
				company = request.POST['company2']
				if company in Company.objects.all():
					company_name = Company.objects.filter(name=company)
					stock.company = company_name[0]
				if company not in Company.objects.all():
					company_name = Company.objects.create(name=company)				
					stock.company = company_name 
			stock.save()
			return redirect('product:list_of_stock')

	return render(request, 'stock/function/create_stock.html', {'stock_form':stock_form, 'address_form':address_form, 'companies':companies})

def ListStock(request):
	stocks = Stock.objects.all()
	return render(request, 'stock/function/list_stock.html', {'stocks':stocks})

def DetailStock(request, pk):
	stock = get_object_or_404(Stock, id=pk)
	return render(request, 'stock/function/detail_stock.html', {'stock':stock})

def DeleteStock(request, pk):
	stock = get_object_or_404(Stock, id=pk)
	if request.method == 'POST':
		stock.delete()
		return redirect('product:list_of_stock')
	return render(request, 'stock/function/delete_stock.html', {'stock':stock})

def UpdateStock(request, pk):
	stock = get_object_or_404(Stock, id=pk)
	stock_form = StockForm(request.POST or None,request.FILES or None, instance=stock)
	address_form = AddressForm(request.POST or None, instance=stock.address)
	companies = Company.objects.all()

	if request.method == 'POST':
		if stock_form.is_valid():
			stock = stock_form.save(commit=False)
			print(address_form.errors)
			if address_form.is_valid():
				address_data = address_form.save()
				stock.address = address_data
			stock.owner = request.user
			company = request.POST['company2']
			if company:
				if company in Company.objects.all():
					company_name = Company.objects.filter(name=company)
					stock.company = company_name[0]
				if company not in Company.objects.all():
					company_name = Company.objects.create(name=company)
					stock.company = company_name	
			else:
				company = request.POST.get('company1', None)
				company_name = Company.objects.filter(name=company)
				stock.company = company_name[0]
			stock.save()
			return redirect('product:details_of_stock', pk=pk)
	return render(request, 'stock/function/update_stock.html', {'stock_form':stock_form, 'address_form':address_form, 'companies':companies, 'stock':stock})


def search(request):
	search_term = ""
	if "search" in request.GET:
		search_term = request.GET['search']
		posts = Post.objects.filter(title__icontains=search_term)
		products = Product.objects.filter(name__icontains=search_term)
		return render(request, 'search.html', {'products':products, 'posts':posts, 'search_term':search_term})

class customerUpdate(UpdateView):
	form_class = CustomerForm
	template_name = 'customer/update.html'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['addressform'] = AddressForm()
		return context

	def form_valid(self, form):
		addressform = AddressForm(self.request.POST)
		customer_data = form.save(commit=False)
		customer_data.save()
		if addressform.is_valid():
			address = addressform.save()
			customer_data.address.add(address)
		return redirect('/')

class customerDetail(DetailView):
	model = Customer
	def get_object(self):
		return get_object_or_404(Customer, pk=self.request.user.id)

def addToCart(request, pk):
	customer = Customer.objects.filter(user=request.user)
	product = get_object_or_404(Product, id=pk)
	customer_cart = Cart.objects.filter(customer=customer[0])	
	if customer_cart:
		customer_cart[0].product.add(product)
	else:
		new_customer_cart = Cart.objects.create(customer=customer[0])
		new_customer_cart.product.add(product)
	return redirect('product:product_detail', pk=pk)

def cart(request):
	customer = Customer.objects.filter(user=request.user)
	customer_cart = Cart.objects.filter(customer=customer[0])
	if customer_cart:
		cart_products = customer_cart[0].product.all()
		price = 0
		for product in cart_products:
			price += product.price
		total_price = price
		total_cart_products = customer_cart[0].product.all().count()
		context = {
					'total_cart_products':total_cart_products,
					'cart_products':cart_products,
					'total_price':price
				}
	else:
		context = {}
	return render(request, 'product/cart.html', context=context)

def removeFromCart(request, pk):
	customer = Customer.objects.filter(user=request.user)
	product = get_object_or_404(Product, id=pk)
	customer_cart = Cart.objects.filter(customer=customer[0])
	if customer_cart:
		customer_cart[0].product.remove(product)
	return redirect('product:cart')
