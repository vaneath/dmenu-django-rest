from rest_framework import viewsets

from apps.vendor.models import Company, Restaurant
from apps.vendor.serializers import CompanySerializer, RestaurantSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
