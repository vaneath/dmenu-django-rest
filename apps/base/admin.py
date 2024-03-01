from django.contrib import admin

from apps.account.models import UserDecorator
from apps.vendor.models import Company, Restaurant

admin.site.register(Company)
admin.site.register(Restaurant)
admin.site.register(UserDecorator)
