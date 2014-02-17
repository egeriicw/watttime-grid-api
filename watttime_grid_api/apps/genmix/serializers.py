from rest_framework import serializers
from apps.griddata.models import DataPoint
from apps.griddata.serializers import BaseDataPointSerializer, BaseDataSeriesSerializer
from apps.genmix.models import Generation


class GenerationSerializer(serializers.HyperlinkedModelSerializer):
    fuel = serializers.SlugRelatedField(slug_field='name')
    class Meta:
        model = Generation
        fields = ('fuel', 'gen_MW')


class GenMixPointSerializer(BaseDataPointSerializer):
    genmix = GenerationSerializer(many=True)

    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'genmix', 'quality', 'url')


class GenMixSeriesSerializer(BaseDataSeriesSerializer):
    datapoints = GenMixPointSerializer(many=True)
