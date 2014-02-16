from rest_framework import viewsets
from apps.genmix.models import DataSeries
from apps.carbon.models import FuelCarbonIntensity
from apps.genmix.views import BaseDataSeriesViewSet
from apps.carbon.serializers import CarbonSeriesSerializer, FuelCarbonIntensitySerializer


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
