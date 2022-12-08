from django.urls import path
from templateApp import views

urlpatterns = [
		path('service/', views.service),
		
]
