from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataSeries, DataPoint
from apps.griddata.serializers import BaseDataPointSerializer, BaseDataSeriesSerializer


class BaseDataSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generic data series to be viewed.
    where -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., where=ISNE
    how -- How the data should be selected.\
        Options are 'past' for historical data\
        or 'best' for best-guess data (historical if available, forecast if not).\
        e.g., how=past
    """
    queryset = DataSeries.objects.all()
    serializer_class = BaseDataSeriesSerializer

    def _filter_confidence(self, qs, confidence):
        if confidence == 'past':
            return qs.filter(series_type=DataSeries.HISTORICAL)
        elif confidence == 'best':
            return qs.filter(series_type=DataSeries.BEST)
        else:
            return qs
            
    def _filter_where(self, qs, where):
        try:
            ba = BalancingAuthority.objects.get(abbrev=where)
            return qs.filter(ba=ba)
        except BalancingAuthority.DoesNotExist:
            return qs        
    
    def filter_queryset(self, queryset):
        # apply all filters in backends
        qs = super(BaseDataSeriesViewSet, self).filter_queryset(queryset)
        
        # filter by confidence
        confidence = self.request.QUERY_PARAMS.get('how', None)
        qs = self._filter_confidence(qs, confidence)
        
        # filter by location
        where = self.request.QUERY_PARAMS.get('where', None)
        qs = self._filter_where(qs, where)
        
        return qs


class BaseDataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    """
    queryset = DataPoint.objects.all()
    serializer_class = BaseDataPointSerializer

