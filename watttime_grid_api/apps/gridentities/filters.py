from django.contrib.gis import forms as geoforms
from apps.gridentities.models import BalancingAuthority
from rest_framework import filters
import django_filters


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
