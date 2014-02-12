from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.gridentities import views

router = routers.DefaultRouter()
router.register(r'balancing_authorities', views.BalancingAuthorityViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)