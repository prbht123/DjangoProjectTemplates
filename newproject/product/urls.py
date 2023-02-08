from django.urls import path 
from product import views 

app_name = 'product'

urlpatterns = [
		path('product_create/', views.productCreate.as_view(), name='product_create'),
		path('product_list/', views.productList.as_view(), name='product_list'),
		path('product_detail/<int:pk>', views.detailProduct.as_view(), name='product_detail'),
		path('product_update/<int:pk>', views.updateProduct.as_view(), name='product_update'),
		path('product_delete/<int:pk>', views.deleteProduct.as_view(), name='product_delete'),
		path('search/', views.search, name='search'),
		path('add_to_cart/<int:pk>', views.addToCart, name='add_to_cart'),
		path('cart/', views.cart, name='cart'),
		path('remove_from_cart/<int:pk>', views.removeFromCart, name='remove_from_cart'),

		# stock
		path('stock_create/', views.createStock.as_view(), name='stock_create'),
		path('stock_list/', views.listStock.as_view(), name='stock_list'),
		path('stock_detail/<int:pk>', views.detailStock.as_view(), name='stock_detail'),
		path('stock_update/<int:pk>', views.updateStock.as_view(), name='stock_update'),
		path('stock_delete/<int:pk>', views.deleteStock.as_view(), name='stock_delete'),

		path('add_to_stock/', views.CreateStock, name='add_to_stock'),
		path('list_of_stock/', views.ListStock, name='list_of_stock'),
		path('details_of_stock/<int:pk>', views.DetailStock, name='details_of_stock'),
		path('delete_of_stock/<int:pk>', views.DeleteStock, name='delete_of_stock'),
		path('update_of_stock/<int:pk>', views.UpdateStock, name='update_of_stock'),

		# customer
		path('customer_detail/', views.customerDetail.as_view(), name='customer_detail'),
		path('customer_update/', views.customerUpdate.as_view(), name='customer_update'),
]