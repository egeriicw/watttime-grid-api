from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.genmix.views import GenMixViewSet
from apps.gridentities.views import BalancingAuthorityViewSet

router = routers.DefaultRouter()
router.register(r'balancing_authorities', BalancingAuthorityViewSet)
router.register(r'genmix', GenMixViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)
