from django.contrib.gis import forms as geoforms
from django.utils.encoding import force_str
from django import forms
from rest_framework import filters, ISO_8601
from rest_framework.compat import parse_datetime
import django_filters
from apps.gridentities.models import BalancingAuthority
from apps.griddata.models import DataPoint
from apps.carbon.models import FuelCarbonIntensity


class GeometryFilter(django_filters.Filter):
    # see https://github.com/djangonauts/django-rest-framework-gis/blob/master/rest_framework_gis/filters.py#L53
    # will be in v0.2 release?
    field_class = geoforms.GeometryField
       
        
class BalancingAuthorityFilter(filters.FilterSet):
    abbrev = django_filters.CharFilter()
    ba_type = django_filters.CharFilter()
    loc = GeometryFilter(name='geom', lookup_type='contains')
    
    class Meta:
        model = BalancingAuthority
        fields = ['abbrev', 'loc', 'ba_type']
        
class FlexibleDateTimeField(forms.DateTimeField):
    # see https://gist.github.com/copitux/5773821
    def strptime(self, value, frmt):
        value = force_str(value)
        parsed = parse_datetime(value)
        if parsed is None: # eg for '2014-03-01'
            return super(FlexibleDateTimeField, self).strptime(value, frmt)
        return parsed

   
class FlexibleDateTimeFilter(django_filters.DateTimeFilter):
    """ Extend ``DateTimeFilter`` to use any date parse-able by dateutil"""    
    field_class = FlexibleDateTimeField


class DataPointFilter(filters.FilterSet):
    # filters for dates
    start_at = FlexibleDateTimeFilter(name='timestamp', lookup_type='gte')
    end_at = FlexibleDateTimeFilter(name='timestamp', lookup_type='lte')
                                             
    # filters for balancing authority
    ba = django_filters.CharFilter(name='ba__abbrev')
  #  loc = GeometryFilter(name='ba__geom', lookup_type='contains')

    class Meta:
        model = DataPoint
        fields = ['start_at', 'end_at', 'ba', 'freq', 'market']


class FuelCarbonFilter(filters.FilterSet):
    # filters for balancing authority
    ba = django_filters.CharFilter(name='ba__abbrev')

    # filter for fuel
    fuel = django_filters.CharFilter(name='fuel__name')
    
    class Meta:
        model = FuelCarbonIntensity
