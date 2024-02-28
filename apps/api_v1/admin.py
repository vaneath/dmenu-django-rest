from django.contrib import admin

from apps.api_v1.models import Company, Restaurant

admin.site.register(Company)
admin.site.register(Restaurant)
