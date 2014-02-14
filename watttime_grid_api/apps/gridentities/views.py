from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.gridentities.serializers import BalancingAuthoritySerializer, FuelTypeSerializer

class BalancingAuthorityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed or edited.
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = BalancingAuthoritySerializer
    filter_fields = ('abbrev', 'ba_type', 'name')


class FuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generation/fuel types to be viewed or edited.
    """
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    filter_fields = ('name',)
