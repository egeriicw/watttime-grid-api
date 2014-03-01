from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.gridentities.serializers import BalancingAuthoritySerializer, FuelTypeSerializer
from apps.gridentities.filters import BalancingAuthorityFilter


class BalancingAuthorityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed.
    abbrev -- Abbreviated name of the balancing authority. e.g., abbrev=ISONE
    ba_type -- Type of balancing authority.\
        Choices are 'ISO' for Independent System Operator (also used for RTOs or similar),\
        or 'BA' for any other balancing authority.\
        e.g., ba_type=ISO
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = BalancingAuthoritySerializer
    filter_class = BalancingAuthorityFilter


class FuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generation/fuel types to be viewed.
    name -- Name of the fuel. e.g., name=wind
    """
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    filter_fields = ('name',)
