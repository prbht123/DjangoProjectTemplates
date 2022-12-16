from django.urls import path
from profileApp import views

app_name='profileApp'

urlpatterns = [
		path('signup/', views.signup, name='signup'),
		path('login/', views.AdminLogin.as_view(), name='login'),
		path('home/', views.home, name='home'),
		path('profile_list/', views.profile_list, name='profile_list'),
		path('profile_detail/<id>', views.profile_detail, name='profile_detail'),
		path('edit_profile/<id>' ,views.edit_profile, name='edit_profile'),
]