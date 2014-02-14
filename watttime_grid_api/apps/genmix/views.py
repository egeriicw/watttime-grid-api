from django.db.models import Q
from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority
from apps.genmix.models import GenMix
from apps.genmix.serializers import GenMixSerializer
from datetime import datetime
import pytz

class BaseGenMixViewSet(viewsets.ModelViewSet):
    """
    Base API endpoint for generation mixes to be viewed or edited.
    """
    serializer_class = GenMixSerializer

    class Meta:
        abstract = True
        

class GenMixViewSet(BaseGenMixViewSet):
    """
    API endpoint that allows all generation mixes to be viewed or edited.
    """
    queryset = GenMix.objects.all()
    
    def _filter_confidence(self, qs, confidence):
        if confidence == 'true':
            return qs.filter(confidence_type=GenMix.TRUE)
        elif confidence == 'best':
            now = pytz.utc.localize(datetime.utcnow())
            return qs.exclude(~Q(confidence_type=GenMix.TRUE),
                                          Q(timestamp__lte=now))
        elif confidence == 'best':
            now = pytz.utc.localize(datetime.utcnow())
            return qs.exclude(~Q(confidence_type=GenMix.TRUE),
                                          Q(timestamp__lte=now))
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
        qs = GenMix.objects.all()
        
        # filter by confidence
        confidence = self.request.QUERY_PARAMS.get('how', None)
        qs = self._filter_confidence(qs, confidence)
        
        # filter by location
        where = self.request.QUERY_PARAMS.get('where', None)
        qs = self._filter_where(qs, where)

        return qs