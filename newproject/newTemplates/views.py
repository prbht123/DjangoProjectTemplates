from django.shortcuts import render

# Create your views here.
def vehicleList(request):
	context = {}
	return render(request, 'vehicle_list.html', context)
	