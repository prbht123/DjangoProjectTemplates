from django.shortcuts import render

# Create your views here.
def service(request):
	context = {}
	return render(request, 'service_template.html', context)

def eBrochure(request):
	context = {}
	return render(request, 'e-brochure.html', context)

def career(request):
	context = {}
	return render(request, 'career.html', context)

def error(request):
	return render(request, 'error.html')

def default(request):
	context = {}
	return render(request, 'default.html', context)

def home(request):
	context = {}
	return render(request, 'home.html', context)

