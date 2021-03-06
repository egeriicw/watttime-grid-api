from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView
from apps.api import views
from apps.api.api_auth import views as auth_views

urlpatterns = patterns('',
    # docs
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('django.swagger.base.view'))),

    # auth
    url(r'^obtain-token-auth/', auth_views.ObtainAuthToken.as_view(),
        name='obtain-token-auth'),
    url(r'^reset-token-auth/', auth_views.ResetAuthToken.as_view(),
        name='reset-token-auth'),

    # data
    url(r'^balancing_authorities/$', views.BalancingAuthorityList.as_view(),
        name='balancingauthority-list'),
    url(r'^balancing_authorities/(?P<abbrev>[A-Z]+)/$', views.BalancingAuthorityDetail.as_view(),
        name='balancingauthority-detail'),
    url(r'^fuels/$', views.FuelTypeList.as_view(),
        name='fueltype-list'),
    url(r'^fuels/(?P<name>[a-z]+)/$', views.FuelTypeDetail.as_view(),
        name='fueltype-detail'),
    url(r'^datapoints/$', views.DataPointList.as_view(),
        name='datapoint-list'),
    url(r'^datapoints/(?P<pk>[0-9]+)/$', views.DataPointDetail.as_view(),
        name='datapoint-detail'),
    url(r'^fuel_carbon_intensities/$', views.FuelToCarbonList.as_view(),
        name='fueltocarbon-list'),
    url(r'^fuel_carbon_intensities/(?P<pk>[0-9]+)/$', views.FuelToCarbonDetail.as_view(),
        name='fueltocarbon-detail'),

    # restricted views
    url(r'^marginal/$', views.DataPointMOERList.as_view(),
        name='datapoint-moer-list'),
    url(r'^marginal/(?P<pk>[0-9]+)/$', views.DataPointMOERDetail.as_view(),
        name='datapoint-moer-detail'),
)
