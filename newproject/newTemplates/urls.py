from django.urls import path
from newTemplates import views
from django.views.generic import TemplateView

app_name = 'newTemplates'

urlpatterns = [
		path('vehicle_list/', views.vehicleList, name='vehicle_list'),
		path('vehicle_details/', views.vehicleDetails, name='vehicle_details'),
		path('product_details/', views.productDetails, name='product_details'),
		path('product_list/', views.productList, name='product_list'),
		path('transporter_list/', TemplateView.as_view(template_name="transporter_list.html"), name='transporter_list'),
		path('transporter_details/', TemplateView.as_view(template_name="transporter_details.html"), name='transporter_details'),	
		]