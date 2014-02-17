from apps.griddata.models import DataSeries
from apps.griddata.views import BaseDataSeriesViewSet
from apps.genmix.serializers import GenMixSeriesSerializer
        
        
class GenMixSeriesViewSet(BaseDataSeriesViewSet):
    """
    API endpoint that allows generation mix data series to be viewed.
    """
    queryset = DataSeries.objects.all()
    serializer_class = GenMixSeriesSerializer
   
