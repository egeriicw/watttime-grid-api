import re
from dateutil.parser import parse as dateutil_parse
from datetime import datetime
import pytz
from rest_framework import viewsets, filters
import django_filters
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataSeries, DataPoint
from apps.griddata.serializers import BaseDataPointSerializer, BaseDataSeriesSerializer


class BaseDataSeriesFilterBackend(filters.BaseFilterBackend):

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
            
    def _filter_when(self, qs, when):
        # default min and max times
        min_timestamp = datetime.min.replace(tzinfo=pytz.utc)
        max_timestamp = datetime.max.replace(tzinfo=pytz.utc)

        try:
            # dates can have alphanumeric, whitespace, colon, comma, period, plus, or minus
            matches = re.search('((?P<start>[a-zA-Z\d\s:+-\.]*),(?P<end>[a-zA-Z\d\s:+-\.]*))', when)
            
            # null matches will be empty strings
            if matches.group('start') != '':
                min_timestamp = dateutil_parse(matches.group('start'))
            if matches.group('end') != '':
                max_timestamp = dateutil_parse(matches.group('end'))
        except TypeError: # when is None
            return qs
            
        filtered = qs.filter(datapoints__timestamp__range=(min_timestamp, max_timestamp))
        for ds in filtered:
            for dp in ds.datapoints.all():
                assert dp.timestamp >= min_timestamp
                assert dp.timestamp <= max_timestamp
        return filtered
    
    def filter_queryset(self, request, queryset, view):
        # filter by confidence
        confidence = request.QUERY_PARAMS.get('how', None)
        queryset = self._filter_confidence(queryset, confidence)
        
        # filter by location
        where = request.QUERY_PARAMS.get('where', None)
        queryset = self._filter_where(queryset, where)
        
        # filter by date
        when = request.QUERY_PARAMS.get('when', None)
        queryset = self._filter_when(queryset, when)
        
        return queryset
        
        
class BaseDataSeriesFilter(django_filters.FilterSet):
    ba = django_filters.CharFilter(name='ba__abbrev')
    start_at = django_filters.DateTimeFilter(name='datapoints__timestamp',
                                             lookup_type='gte')
 #   end_at = django_filters.DateTimeFilter(name='datapoints__timestamp',
 #                                          lookup_type='lte')
                                           
    class Meta:
        model = DataSeries
        fields = ['ba', 'series_type', 'start_at'] #, 'end_at']


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
    queryset = DataSeries.objects.all()
    serializer_class = BaseDataSeriesSerializer
   # filter_backends = (BaseDataSeriesFilterBackend, filters.DjangoFilterBackend,)
    filter_class = BaseDataSeriesFilter


class BaseDataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    """
    queryset = DataPoint.objects.all()
    serializer_class = BaseDataPointSerializer

