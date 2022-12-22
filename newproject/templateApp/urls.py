from django.urls import path
from templateApp import views
app_name = 'templateApp'

urlpatterns = [
		path('service/', views.service),
		path('vehicle_details/',views.vehicleDetails),
		
]
