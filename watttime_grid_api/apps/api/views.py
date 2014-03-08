from rest_framework import generics, viewsets
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.carbon.models import FuelCarbonIntensity
from apps.api import serializers, filters


class BalancingAuthorityList(generics.ListAPIView):
    """
    API endpoint that allows a list of balancing authorities to be viewed.
    abbrev -- Abbreviated name of the balancing authority.\
        e.g., abbrev=ISONE
    ba_type -- Type of balancing authority.\
        Choices are 'ISO' for Independent System Operator (also used for RTOs or similar),\
        or 'BA' for any other balancing authority.\
        e.g., ba_type=ISO
    loc -- Location within balancing authority, in GeoJSON or WKT.\
        e.g., loc={"type": "Point", "coordinates": [ -72.519, 42.372]}\
        or loc=POINT (-72.519 42.372)
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = serializers.BalancingAuthoritySerializer
    filter_class = filters.BalancingAuthorityFilter
    lookup_field = 'abbrev'


class BalancingAuthorityDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a single balancing authority to be viewed.
    """
    queryset = BalancingAuthority.objects.all()
    serializer_class = serializers.BalancingAuthoritySerializer
    lookup_field = 'abbrev'


class FuelTypeList(generics.ListAPIView):
    """
    API endpoint that allows a list of generation/fuel types to be viewed.
    name -- Name of the fuel. e.g., name=wind
    is_renewable -- 'True' returns only renewable fuels,\
        'False' returns non-renewable and unspecified fuels.
    is_fossil -- 'True' returns only fossil fuels,\
        'False' returns non-fossil and unspecified fuels.
    """
    queryset = FuelType.objects.all()
    serializer_class = serializers.FuelTypeSerializer
    filter_fields = ('name', 'is_renewable', 'is_fossil')
    lookup_field = 'name'


class FuelTypeDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a single generation/fuel type to be viewed.
    """
    queryset = FuelType.objects.all()
    serializer_class = serializers.FuelTypeSerializer
    lookup_field = 'name'


class DataPointList(generics.ListAPIView):
    """
    API endpoint that allows a list of grid data points to be viewed.
    All times are in UTC. 'carbon' is in lb CO2/MW.
    
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., ba=ISONE
    start_at -- Minimum timestamp (inclusive).\
        e.g., start_at=2014-02-20 \
        or start_at=2014-02-20T16:45:30-0800 \
        or start_at=2014-02-20T16:45:30-08:00
    end_at -- Maximum timestamp (inclusive).\
        e.g., end_at=2014-02-20 \
        or end_at=2014-02-20T16:45:30-0800 \
        or end_at=2014-02-20T16:45:30-08:00
    page_size -- Number of data points to return on each page.\
        default is page_size=12
    freq -- Time series frequency.\
        Options are '5m', '10m', '1hr', 'n/a'.\
        e.g., freq=1hr
    market -- Market from which the data were gathered.\
        Options are 'RT5M' for real-time 5 minute,\
        'RTHR' for real-time hourly,\
        or 'DAHR' for day-ahead hourly.
        e.g., market=RT5M
    """
    queryset = DataPoint.objects.all()
    serializer_class = serializers.DataPointSerializer
    filter_class = filters.DataPointFilter
    
    # turn on pagination
    paginate_by = 12
    paginate_by_param = 'page_size'
    
    
class DataPointDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a single grid data point to be viewed.
    All times are in UTC. 'carbon' is in lb CO2/MW.
    'pk' is a unique numeric identifier for a data point.
    """
    queryset = DataPoint.objects.all()
    serializer_class = serializers.DataPointSerializer    


class FuelToCarbonList(generics.ListAPIView):
    """
    API endpoint that allows a list of fuel-to-carbon conversions to be viewed.
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        If 'null', this value will be used as a default for balancing authorities\
            for which no conversion is specified.\
        e.g., ba=ISONE
    fuel -- A name for a fuel.\
        Options can be found at the 'fuels' endpoint.\
        e.g., fuel=wind
    """
    queryset = FuelCarbonIntensity.objects.all()
    serializer_class = serializers.FuelCarbonIntensitySerializer
    filter_class = filters.FuelCarbonFilter


class FuelToCarbonDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a single fuel-to-carbon conversion to be viewed.
    'pk' is a unique numeric identifier for a conversion.
    """
    queryset = FuelCarbonIntensity.objects.all()
    serializer_class = serializers.FuelCarbonIntensitySerializer
