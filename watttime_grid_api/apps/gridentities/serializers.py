from apps.gridentities.models import BalancingAuthority, FuelType
from rest_framework import serializers


class BalancingAuthoritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BalancingAuthority
        fields = ('name', 'ba_type', 'url', 'abbrev', 'link')

class FuelTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FuelType
