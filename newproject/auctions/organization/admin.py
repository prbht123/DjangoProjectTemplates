from django.contrib import admin
from auctions.organization.models import Organization, Industry

# Register your models here.
admin.site.register(Organization)
admin.site.register(Industry)