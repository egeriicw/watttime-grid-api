import django_filters
from rest_framework_chain import ChainedFilterSet, RelatedFilter
from apps.griddata.models import DataSeries, DataPoint
from apps.gridentities.filters import BalancingAuthorityFilter


class BaseDataPointFilter(ChainedFilterSet):
    start_at = django_filters.DateTimeFilter(name='timestamp',
                                             lookup_type='gte')
    end_at = django_filters.DateTimeFilter(name='timestamp',
                                             lookup_type='lte')

    class Meta:
        model = DataPoint
        fields = ['start_at', 'end_at']


class BaseDataSeriesFilter(ChainedFilterSet):
    # propagate BA filters
    ba = RelatedFilter(BalancingAuthorityFilter, name='abbrev')
    loc = RelatedFilter(BalancingAuthorityFilter, name='loc')

    # propagate time filters
   # start_at = RelatedFilter(BaseDataPointFilter, name='datapoints__start_at')
   # end_at = RelatedFilter(BaseDataPointFilter, name='datapoints__end_at')
    start_at = django_filters.DateTimeFilter(name='datapoints__timestamp', lookup_type='gte')
    end_at = django_filters.DateTimeFilter(name='datapoints__timestamp', lookup_type='lte')
                                           
    class Meta:
        model = DataSeries
        fields = ['ba', 'series_type', 'start_at', 'end_at', 'loc']
