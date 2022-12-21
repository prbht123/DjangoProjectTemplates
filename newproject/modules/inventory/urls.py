from django.urls import path
from modules.inventory import views

app_name = 'inventory'

urlpatterns = [
		path('add_product/', views.ProductCreateView.as_view(), name='add_product'),
		path('product_list/', views.ProductListView.as_view(), name='product_list'),
		path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
		path('update_product/<int:pk>', views.ProductUpdateView.as_view(), name='update_product'),
		path('delete_product/<int:pk>', views.ProductDeleteView.as_view(), name='delete_product'),
		]