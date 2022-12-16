from django.shortcuts import render, redirect
from auctions.organization.models import Organization, Industry
from auctions.organization.forms import OrganizationForm, IndustryForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

class organizationAddView(LoginRequiredMixin,CreateView):
	login_url = 'profileApp:login'
	redirect_field_name = 'redirect_to'
	form_class = OrganizationForm
	template_name = 'organization/create.html'

	def form_valid(self, form):
		data = form.save(commit=False)
		data.save()
		industry = self.request.POST['industry']
		industries = industry.split(',')
		for value in industries:
			var = Industry.objects.filter(title=value)
			if var:
				data.industry.add(var[0])
			else:
				data.industry.create(title=value)		
		return redirect('organization:organization_list')

class organizationListView(ListView):
	model = Organization
	template_name = 'organization/list.html'
	context_object_name = 'organization_list'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		context['industry'] = Industry.objects.all()
		return context

class organizationDetailView(DetailView):
	model = Organization
	template_name = 'organization/detail.html'
	context_object_name = 'organization'

class organizationUpdateView(LoginRequiredMixin, UpdateView):
	login_url = 'profileApp:login'
	redirect_field_name = 'redirect_to'
	model = Organization
	form_class = OrganizationForm
	template_name = 'organization/update.html'
	pk_url_kwarg = 'pk'

	def form_valid(self, form):
		data = form.save(commit=False)
		data.save()
		industry = self.request.POST['industry']
		industries = industry.split(',')
		for value in industries:
			var = Industry.objects.filter(title=value)
			if var in data.industry.all():
				continue				
			else:
				if var:
					data.industry.add(var[0])
				else:
					data.industry.create(title=value)		
		return redirect('organization:organization_list')

class organizationDeleteView(DeleteView):
	model = Organization
	template_name = 'organization/delete.html'
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('organization:organization_list')

	



