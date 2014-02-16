from apps.genmix.models import DataPoint, DataSeries, Generation
from apps.gridentities.serializers import BalancingAuthoritySerializer
from rest_framework import serializers

class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    fuel = serializers.SlugRelatedField(slug_field='name')
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class BaseDataPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'quality', 'url')


class GenMixPointSerializer(BaseDataPointSerializer):
    genmix = GenerationSerializer(many=True)

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'genmix', 'quality', 'url')


class BaseDataSeriesSerializer(serializers.HyperlinkedModelSerializer):
    datapoints = BaseDataPointSerializer(many=True)
    ba = BalancingAuthoritySerializer

    class Meta:
        model = DataSeries
        fields = ('ba', 'series_type', 'datapoints') #, 'url')
        depth = 2


class GenMixSeriesSerializer(BaseDataSeriesSerializer):
    datapoints = GenMixPointSerializer(many=True)
