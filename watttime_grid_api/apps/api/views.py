from rest_framework import viewsets
from apps.gridentities.models import BalancingAuthority, FuelType
from apps.griddata.models import DataPoint
from apps.api import serializers, filters


class BalancingAuthorityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows balancing authorities to be viewed.
    abbrev -- Abbreviated name of the balancing authority..\
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


class FuelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows generation/fuel types to be viewed.
    name -- Name of the fuel. e.g., name=wind
    """
    queryset = FuelType.objects.all()
    serializer_class = serializers.FuelTypeSerializer
    filter_fields = ('name',)


class DataPointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows grid data points to be viewed.
    ba -- An abbreviation for a balancing authority.\
        Options can be found at the 'balancing_authorities' endpoint.\
        e.g., ba=ISONE
    start_at -- Minimum date-time (inclusive).\
        e.g., start_at=2014-02-20 \
        or start_at=2014-02-20T16:45:30-0800 \
        or start_at=2014-02-20T16:45:30-08:00
    end_at -- Maximum date-time (inclusive).\
        e.g., end_at=2014-02-20 \
        or end_at=2014-02-20T16:45:30-0800 \
        or end_at=2014-02-20T16:45:30-08:00
    page_size -- Number of data points to return on each page.\
        default is page_size=12
    freq -- Time series frequency.\
        Options are '5m', '10m', '1hr', 'n/a'.\
        e.g., freq=1hr
    """
    queryset = DataPoint.objects.all()
    serializer_class = serializers.DataPointSerializer
    filter_class = filters.DataPointFilter
    
    # turn on pagination
    paginate_by = 12
    paginate_by_param = 'page_size'
