from apps.griddata.models import DataSeries
from apps.griddata.views import BaseDataSeriesViewSet
from apps.genmix.serializers import GenMixSeriesSerializer
        
        
class GenMixSeriesViewSet(BaseDataSeriesViewSet):
    """
    API endpoint that allows generation mix data series to be viewed.
    where -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., where=ISNE
    how -- How the data should be selected.\
        Options are 'past' for historical data\
        or 'best' for best-guess data (historical if available, forecast if not).\
        e.g., how=past
    """
    queryset = DataSeries.objects.all()
    serializer_class = GenMixSeriesSerializer
   
