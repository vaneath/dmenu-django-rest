from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.account.urls')),
    path('api/v1/vendor', include('apps.vendor.urls')),
]
