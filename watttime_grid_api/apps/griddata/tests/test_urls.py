from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.griddata.views import BaseDataSeriesViewSet, BaseDataPointViewSet


router = routers.DefaultRouter()
router.register(r'test_series', BaseDataSeriesViewSet)
router.register(r'datapoints', BaseDataPointViewSet, base_name='datapoint')

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
