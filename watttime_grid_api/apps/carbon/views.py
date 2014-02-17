from rest_framework import viewsets
from apps.griddata.models import DataSeries, DataPoint
from apps.griddata.views import BaseDataSeriesViewSet
from apps.carbon.models import FuelCarbonIntensity
from apps.carbon.serializers import CarbonSeriesSerializer, FuelCarbonIntensitySerializer, FullDataPointSerializer


class FuelToCarbonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows fuel-to-carbon conversions to be viewed.
    """
    queryset = FuelCarbonIntensity.objects.all()
    serializer_class = FuelCarbonIntensitySerializer


class CarbonSeriesViewSet(BaseDataSeriesViewSet):
    """
    API endpoint that allows carbon intensity data series to be viewed.
    """
    queryset = DataSeries.objects.all()
    serializer_class = CarbonSeriesSerializer


class FullDataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    """
    queryset = DataPoint.objects.all()
    serializer_class = FullDataPointSerializer

