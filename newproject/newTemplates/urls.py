from django.urls import path
from newTemplates import views

app_name = 'newTemplates'

urlpatterns = [
		path('vehicle_list/', views.vehicleList, name='vehicle_list'),
		]