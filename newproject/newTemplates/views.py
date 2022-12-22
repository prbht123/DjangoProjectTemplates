from django.shortcuts import render

# Create your views here.
def vehicleList(request):
	context = {}
	return render(request, 'vehicle_list.html', context)

def productList(request):
	context = {}
	return render(request, 'product_list.html', context)

def productDetails(request):
	context = {}
	return render(request, 'product_details.html', context)
	