from apps.gridentities.serializers import BalancingAuthoritySerializer, FuelTypeSerializer
from apps.griddata.models import DataPoint
from apps.griddata.serializers import BaseDataSeriesSerializer, BaseDataPointSerializer
from apps.genmix.serializers import GenerationSerializer
from apps.carbon.models import FuelCarbonIntensity
from rest_framework import serializers


class FuelCarbonIntensitySerializer(serializers.HyperlinkedModelSerializer):
    ba = BalancingAuthoritySerializer()
    fuel = FuelTypeSerializer()

    class Meta:
        model = FuelCarbonIntensity
        fields = ('valid_after', 'lb_CO2_per_MW', 'fuel', 'ba')


class CarbonPointSerializer(BaseDataPointSerializer):
 #   carbon = serializers.RelatedField(read_only=True)
    carbon = serializers.SerializerMethodField('get_carbon')

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'quality', 'url')
        
    def get_carbon(self, obj):
        try:
            return round(obj.carbon.emissions_intensity, 1)
        except:
            return None

        
class CarbonSeriesSerializer(BaseDataSeriesSerializer):
    datapoints = CarbonPointSerializer(many=True)


class FullDataPointSerializer(BaseDataPointSerializer):
    carbon = serializers.SerializerMethodField('get_carbon')
    genmix = GenerationSerializer(many=True)
    ba = BalancingAuthoritySerializer()

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'quality', 'genmix', 'url',
                  'market', 'freq', 'is_marginal', 'ba')

    def get_carbon(self, obj):
        try:
            return round(obj.carbon.emissions_intensity, 1)
        except:
            return None
