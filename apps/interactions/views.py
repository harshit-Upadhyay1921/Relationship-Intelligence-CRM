from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Interaction
from .serializers import InteractionSerializer

permission_classes = [AllowAny]

class InteractionViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.all()
    serializer_class = InteractionSerializer
