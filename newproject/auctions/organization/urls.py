from django.urls import path
from auctions.organization import views

app_name = 'organization'

urlpatterns = [
		path('add_organization/', views.organizationAddView.as_view(), name='add_organization'),
		path('organization_list/', views.organizationListView.as_view(), name='organization_list'),
		path('organization_detail/<int:pk>', views.organizationDetailView.as_view(), name='organization_detail'),
		path('update_organization/<int:pk>', views.organizationUpdateView.as_view(), name='update_organization'),
		path('delete_organization/<int:pk>', views.organizationDeleteView.as_view(), name='delete_organization'),
		]