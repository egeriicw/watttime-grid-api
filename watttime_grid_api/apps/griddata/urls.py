from django.conf.urls import patterns, url
from apps.griddata import views


urlpatterns = patterns('',
    # dashboard views
    url(r'map/',
        views.CurrentMapView.as_view(template_name="map.html"),
        name='map'),
  #  url(r'dashboard/',
  #     views.DashboardView.as_view(template_name="dashboard.html"),
  #      name='dashboard'),
)