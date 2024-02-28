from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.api_v1 import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')


urlpatterns = [
  path('', include(router.urls)),
]
