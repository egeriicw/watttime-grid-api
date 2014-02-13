from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.genmix import views as genmix_views
from apps.gridentities import views as ge_views

router = routers.DefaultRouter()
router.register(r'balancing_authorities', ge_views.BalancingAuthorityViewSet)
router.register(r'genmix', genmix_views.AllGenMixViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)