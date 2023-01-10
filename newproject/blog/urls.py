from django.urls import path
from blog import views
from blog import portal

app_name = 'blog'

urlpatterns = [
		path('post_create/', views.createPost.as_view(), name='post_create'),
		path('post_list/', views.listPost.as_view(), name='post_list'),
		path('all_post_list/', views.allListPost.as_view(), name='all_post_list'),
		path('post_detail/<int:pk>', views.detailPost.as_view(), name='post_detail'),
		path('post_update/<int:pk>', views.updatePost.as_view(), name='post_update'),
		path('post_delete/<int:pk>', views.deletePost.as_view(), name='post_delete'),

		
]