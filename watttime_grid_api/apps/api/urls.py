from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.genmix.views import GenMixSeriesViewSet
from apps.gridentities.views import BalancingAuthorityViewSet, FuelTypeViewSet
from apps.carbon.views import CarbonSeriesViewSet, FuelToCarbonViewSet, FullDataPointViewSet

router = routers.DefaultRouter()
router.register(r'balancing_authorities', BalancingAuthorityViewSet)
router.register(r'fuels', FuelTypeViewSet)
router.register(r'genmix', GenMixSeriesViewSet, base_name='genmix')
router.register(r'datapoints', FullDataPointViewSet, base_name='datapoint')
router.register(r'fuel_to_carbon', FuelToCarbonViewSet)
router.register(r'carbon', CarbonSeriesViewSet, base_name='carbon')

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
