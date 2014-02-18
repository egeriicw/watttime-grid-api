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
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., ba=ISNE
    series_type -- How the data should be selected.\
        Options are 'PAST' for historical data\
        or 'BEST' for best-guess data (historical if available, forecast if not).\
        e.g., series_type=PAST
    """
    queryset = DataSeries.objects.all()
    serializer_class = CarbonSeriesSerializer


class FullDataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    """
    queryset = DataPoint.objects.all()
    serializer_class = FullDataPointSerializer

