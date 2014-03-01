from rest_framework import viewsets
from apps.griddata.models import DataSeries, DataPoint
from apps.griddata.serializers import BaseDataPointSerializer, BaseDataSeriesSerializer
from apps.griddata.filters import BaseDataSeriesFilter


class BaseDataSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., ba=ISNE
    series_type -- How the data should be selected.\
        Options are 'PAST' for historical data\
        or 'BEST' for best-guess data (historical if available, forecast if not).\
        e.g., series_type=PAST
    """
    queryset = DataSeries.objects.all().prefetch_related('datapoints')
    serializer_class = BaseDataSeriesSerializer
    filter_class = BaseDataSeriesFilter


class BaseDataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    """
    queryset = DataPoint.objects.all()
    serializer_class = BaseDataPointSerializer

