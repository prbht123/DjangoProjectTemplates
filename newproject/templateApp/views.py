from django.shortcuts import render

# Create your views here.
def service(request):
	context = {'name':'Piu', 'company':'Webkrone'}
	return render(request, 'service_template.html', context)