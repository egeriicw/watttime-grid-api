from django.conf.urls import patterns, url, include
from rest_framework import routers
from apps.api import views

router = routers.DefaultRouter()
router.register(r'balancing_authorities', views.BalancingAuthorityViewSet)
router.register(r'fuels', views.FuelTypeViewSet)
router.register(r'datapoints', views.DataPointViewSet, base_name='datapoint')
#router.register(r'fuel_to_carbon', FuelToCarbonViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^docs/', include('rest_framework_swagger.urls')),
)
