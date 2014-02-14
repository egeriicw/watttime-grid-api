from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority, GenType
from apps.gridentities.serializers import BalancingAuthoritySerializer, GenTypeSerializer

class BalancingAuthorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed or edited.
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = BalancingAuthoritySerializer
    filter_fields = ('abbrev', 'ba_type', 'name')


class GenTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows generation/fuel types to be viewed or edited.
    """
    queryset = GenType.objects.all()
    serializer_class = GenTypeSerializer
    filter_fields = ('name',)
