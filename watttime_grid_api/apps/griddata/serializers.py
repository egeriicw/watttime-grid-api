from rest_framework import serializers
from apps.gridentities.serializers import BalancingAuthoritySerializer
from apps.griddata.models import DataPoint, DataSeries


class BaseDataPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataPoint
        fields = ('timestamp', 'created_at', 'quality', 'url')


class BaseDataSeriesSerializer(serializers.HyperlinkedModelSerializer):
    datapoints = BaseDataPointSerializer(many=True)
    ba = BalancingAuthoritySerializer

    class Meta:
        model = DataSeries
        fields = ('ba', 'series_type', 'datapoints') #, 'url')
        depth = 2

