from django import forms
from auctions.organization.models import Organization, Industry

class OrganizationForm(forms.ModelForm):
	class Meta:
		model = Organization
		fields = ['name','website','organization_type','founder','founded','headquarter','description','area_served','image']

class IndustryForm(forms.ModelForm):
	class Meta:
		model = Industry
		fields = {'title'}