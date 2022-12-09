from django.urls import path
from templateApp import views

urlpatterns = [
		path('service/', views.service),
		path('e_brochure/', views.eBrochure),
		path('career/', views.career),
		path('error/', views.error),
		path('default/', views.default),
		path('', views.home),
		
]
