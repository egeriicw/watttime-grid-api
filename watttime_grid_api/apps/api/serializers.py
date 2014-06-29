from rest_framework import serializers
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint, CurrentDataSet
from apps.supply_demand.models import Generation, Load
from apps.carbon.models import FuelCarbonIntensity
from apps.marginal.models import MOER


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


class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = ('value', 'units',)


class FuelCarbonIntensitySerializer(serializers.HyperlinkedModelSerializer):
    ba = BalancingAuthoritySerializer()
    fuel = serializers.SlugRelatedField(slug_field='name')

    class Meta:
        model = FuelCarbonIntensity
        fields = ('valid_after', 'lb_CO2_per_MW', 'fuel', 'ba')


class MOERSerializer(serializers.ModelSerializer):
    structural_model = serializers.RelatedField(source='structural_model.algorithm.description')

    class Meta:
        model = MOER
        fields = ('value', 'units', 'structural_model')


class DataPointSerializer(serializers.HyperlinkedModelSerializer):
    carbon = serializers.SlugRelatedField(slug_field='emissions_intensity',
                                          help_text='average carbon emissions intensity, in lb/MW')
    genmix = GenerationSerializer(many=True)
    ba = serializers.SlugRelatedField(slug_field='abbrev',
                                      help_text='abbreviated name of the balancing authority')

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'carbon', 'genmix', 'url',
                  'market', 'freq', 'ba')


class DataPointMOERSerializer(DataPointSerializer):
    moer_set = MOERSerializer()
    load_set = LoadSerializer()

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'genmix', 'url',
                  'market', 'freq', 'ba', 'moer_set', 'load_set')


class DataPointInSeriesSerializer(DataPointMOERSerializer):
    class Meta:
        model = DataPoint
        fields = ('timestamp', 'genmix', 'url',
                  'market', 'moer_set')


class CurrentDataSetSerializer(serializers.ModelSerializer):
    past = DataPointInSeriesSerializer(many=True)
    forecast = DataPointInSeriesSerializer(many=True)
    current = DataPointInSeriesSerializer()
    ba = serializers.SlugRelatedField(slug_field='abbrev',
                                      help_text='abbreviated name of the balancing authority')

    class Meta:
        model = CurrentDataSet
        fields = ('past', 'forecast', 'current', 'ba')
