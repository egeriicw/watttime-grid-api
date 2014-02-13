from django.db.models import Q
from rest_framework import viewsets
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
        

class AllGenMixViewSet(BaseGenMixViewSet):
    """
    API endpoint that allows all generation mixes to be viewed or edited.
    """
    queryset = GenMix.objects.all()


class TrueGenMixViewSet(BaseGenMixViewSet):
    """
    API endpoint that allows true generation mixes to be viewed or edited.
    """
    queryset = GenMix.objects.filter(confidence_type=GenMix.TRUE)


class BestGuessGenMixViewSet(BaseGenMixViewSet):
    """
    API endpoint that allows best-guess generation mixes to be viewed or edited.
    """
    now = pytz.utc.localize(datetime.utcnow())
    queryset = GenMix.objects.exclude(~Q(confidence_type=GenMix.TRUE),
                                      Q(timestamp__lte=now))
