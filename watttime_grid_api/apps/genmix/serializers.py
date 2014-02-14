from apps.genmix.models import DataPoint, DataSeries, Generation
from apps.gridentities.serializers import BalancingAuthoritySerializer
from rest_framework import serializers

class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    fuel = serializers.SlugRelatedField(slug_field='name')
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class DataPointSerializer(serializers.HyperlinkedModelSerializer):
    genmix = GenerationSerializer(many=True)

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'url', 'genmix', 'quality')


class DataSeriesSerializer(serializers.HyperlinkedModelSerializer):
    datapoints = DataPointSerializer(many=True)
    ba = BalancingAuthoritySerializer()

    class Meta:
        model = DataSeries
        fields = ('ba', 'series_type', 'url', 'datapoints')
        depth = 2

