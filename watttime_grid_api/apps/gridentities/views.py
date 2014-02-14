from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority
from apps.gridentities.serializers import BalancingAuthoritySerializer

class BalancingAuthorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed or edited.
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = BalancingAuthoritySerializer
    filter_fields = ('abbrev', 'ba_type', 'name')
