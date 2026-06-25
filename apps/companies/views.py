from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Company
from .serializers import CompanySerializer

permission_classes = [AllowAny]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
