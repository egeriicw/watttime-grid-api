from apps.gridentities.serializers import BalancingAuthoritySerializer, FuelTypeSerializer
from apps.genmix.models import DataPoint
from apps.genmix.serializers import BaseDataSeriesSerializer, BaseDataPointSerializer, GenerationSerializer
from apps.carbon.models import FuelCarbonIntensity
from rest_framework import serializers


class FuelCarbonIntensitySerializer(serializers.HyperlinkedModelSerializer):
    ba = BalancingAuthoritySerializer()
    fuel = FuelTypeSerializer()

    class Meta:
        model = FuelCarbonIntensity
        fields = ('valid_after', 'lb_CO2_per_MW', 'fuel', 'ba')


class CarbonPointSerializer(BaseDataPointSerializer):
    carbon = serializers.RelatedField(read_only=True)

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'quality', 'url')

        
class CarbonSeriesSerializer(BaseDataSeriesSerializer):
    datapoints = CarbonPointSerializer(many=True)


class FullDataPointSerializer(BaseDataPointSerializer):
    carbon = serializers.RelatedField(read_only=True)
    genmix = GenerationSerializer(many=True)

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'quality', 'genmix', 'url')
