from django.contrib.gis import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, ListView
from djgeojson.views import GeoJSONLayerView
from apps.gridentities.models import BalancingAuthority
import json
from datetime import datetime
import pytz

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

class GeoJSONTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(GeoJSONTemplateView, self).get_context_data(**kwargs)
        geojson = {}
     #   geojson["crs"] = {"type": "link",
     #                       "properties": {"href": "http://spatialreference.org/ref/epsg/4326/", "type": "proj4"}}
     #   geojson["type"] = "FeatureCollection"
        geojson["features"] = []
        for row in BalancingAuthority.objects.all():
            try:
                dp = row.datapoint_set.filter(quality="PAST").latest()
                carbon_val = round(dp.carbon.emissions_intensity, 1)
                td = (pytz.utc.localize(datetime.utcnow()) - dp.timestamp).seconds / 60
            except:
                carbon_val = 0
                td = None
            try:
                properties = {'name': str(row),
                              'carbon': carbon_val,
                              'lag': td,
                              }
                geojson["features"].append({'geometry': json.loads(row.geom.geojson),
                                            'properties': properties,
                                            'type': "Feature",
                                            'id': row.id,
                                            })
            except AttributeError: # no geom
                continue
        context['geojson'] = json.dumps(geojson).replace('\\','')
        return context
        

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # home
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^contact/', TemplateView.as_view(template_name="contact.html"), name='contact'),
    url(r'^map/',
        GeoJSONTemplateView.as_view(template_name="map.html"),
        name='map'),
    url(r'^ba.geojson',
        GeoJSONLayerView.as_view(model=BalancingAuthority,
                                 properties=('abbrev', 'name')),
        name='ba_geom'),

    # api
    url(r'^api/v1/', include('apps.api.urls')),

    # api docs
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
