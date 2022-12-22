from django.urls import path
from newTemplates import views

app_name = 'newTemplates'

urlpatterns = [
		path('vehicle_list/', views.vehicleList, name='vehicle_list'),
		path('product_details/', views.productDetails, name='product_details'),
		path('product_list/', views.productList, name='product_list'),
		]