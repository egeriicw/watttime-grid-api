#from django.db.models import Q
from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority
from apps.genmix.models import DataPoint, DataSeries
from apps.genmix.serializers import DataSeriesSerializer, DataPointSerializer
#from datetime import datetime
#import pytz


class DataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows data points to be viewed or edited.
    """
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer


class GenMixViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generation mix data series to be viewed or edited.
    """
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer
    
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
    
    def get_queryset(self):
        # set up initial queryset
        qs = DataSeries.objects.all()
        
        # filter by confidence
        confidence = self.request.QUERY_PARAMS.get('how', None)
        qs = self._filter_confidence(qs, confidence)
        
        # filter by location
        where = self.request.QUERY_PARAMS.get('where', None)
        qs = self._filter_where(qs, where)

        return qs
