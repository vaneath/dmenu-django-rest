from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api_v1 import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')


urlpatterns = [
  path('', include(router.urls)),
]
