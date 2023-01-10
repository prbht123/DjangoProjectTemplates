from django.shortcuts import render

# Create your views here.
def service(request):
	context = {'name':'Piu', 'company':'Webkrone'}
	return render(request, 'service_template.html', context)

def vehicleDetails(request):
	context = {}
	return render(request, 'vehicle_details_1.html', context)