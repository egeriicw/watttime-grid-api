from apps.griddata.models import DataSeries
from apps.griddata.views import BaseDataSeriesViewSet
from apps.genmix.serializers import GenMixSeriesSerializer
        
        
class GenMixSeriesViewSet(BaseDataSeriesViewSet):
    """
    API endpoint that allows generation mix data series to be viewed.\
        All generation values have units of MW power produced.
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., ba=ISONE
    series_type -- How the data should be selected.\
        Options are 'PAST' for historical data\
        or 'BEST' for best-guess data (historical if available, forecast if not).\
        e.g., series_type=PAST
    """
  #  queryset = DataSeries.objects.all()
    serializer_class = GenMixSeriesSerializer
   
