from rest_framework import viewsets
from apps.gridentities.models import GridEntity
from apps.gridentities.serializers import GridEntitySerializer

class BalancingAuthorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed or edited.
    """
    queryset = GridEntity.objects.filter(entity_type__in=[GridEntity.BA, GridEntity.ISO])
    serializer_class = GridEntitySerializer
