#from django.db.models import Q
from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority
from apps.genmix.models import DataPoint, DataSeries
from apps.genmix.serializers import GenMixSeriesSerializer, GenMixPointSerializer
#from datetime import datetime
#import pytz


class BaseDataSeriesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generic data series to be viewed.
    """
    class Meta:
        abstract = True

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
    
    def filter_queryset(self):
        # set up initial queryset
        qs = self.get_queryset()

        # apply all filters in backends
        qs = super(BaseDataSeriesViewSet, self).filter_queryset()
        
        # filter by confidence
        confidence = self.request.QUERY_PARAMS.get('how', None)
        qs = self._filter_confidence(qs, confidence)
        
        # filter by location
        where = self.request.QUERY_PARAMS.get('where', None)
        qs = self._filter_where(qs, where)
        
        return qs
        
        
class GenMixSeriesViewSet(BaseDataSeriesViewSet):
    """
    API endpoint that allows generation mix data series to be viewed.
    """
    queryset = DataSeries.objects.all()
    serializer_class = GenMixSeriesSerializer
   
