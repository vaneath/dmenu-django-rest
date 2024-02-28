from rest_framework import viewsets

from apps.api_v1.models import Company
from apps.api_v1.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
