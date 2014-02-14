from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.genmix.views import GenMixViewSet, DataPointViewSet
from apps.gridentities.views import BalancingAuthorityViewSet, GenTypeViewSet

router = routers.DefaultRouter()
router.register(r'balancing_authorities', BalancingAuthorityViewSet)
router.register(r'fuels', GenTypeViewSet)
router.register(r'genmix', GenMixViewSet)
router.register(r'datapoints', DataPointViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
