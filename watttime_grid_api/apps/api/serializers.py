from rest_framework import serializers
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.genmix.models import Generation
from apps.carbon.models import FuelCarbonIntensity


class BalancingAuthoritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BalancingAuthority
        fields = ('name', 'ba_type', 'url', 'abbrev', 'link', 'notes')
        lookup_field = 'abbrev'
        

class FuelTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FuelType
        lookup_field = 'name'


class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    fuel = serializers.SlugRelatedField(slug_field='name')
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class FuelCarbonIntensitySerializer(serializers.HyperlinkedModelSerializer):
    ba = BalancingAuthoritySerializer()
    fuel = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = FuelCarbonIntensity
        fields = ('valid_after', 'lb_CO2_per_MW', 'fuel', 'ba')


class DataPointSerializer(serializers.HyperlinkedModelSerializer):
    carbon = serializers.SlugRelatedField(slug_field='emissions_intensity',
                                          help_text='carbon emissions intensity, in lb/MW')
    genmix = GenerationSerializer(many=True)
    ba = serializers.SlugRelatedField(slug_field='abbrev',
                                      help_text='abbreviated name of the balancing authority')

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'genmix', 'url',
                  'market', 'freq', 'ba')
