from django.views.generic import TemplateView
from apps.griddata.models import DataSeries
import json
from datetime import datetime
import pytz


class CurrentMapView(TemplateView):
    def get_context_data(self, **kwargs):
        # get other context
        context = super(CurrentMapView, self).get_context_data(**kwargs)
        
        # set up geojson
        geojson = {}
        geojson["features"] = []
        
        
        for ds in DataSeries.objects.filter(series_type=DataSeries.CURRENT):
            # get vals
            try:
                dp = ds.datapoints.latest()
                carbon_val = round(dp.carbon.emissions_intensity, 0)
                td = (pytz.utc.localize(datetime.utcnow()) - dp.timestamp).seconds / 60
            except:
                carbon_val = 0
                td = None
            try:
                ba = ds.ba
                properties = {'name': str(ba),
                              'carbon': carbon_val,
                              'lag': td,
                              }
                geojson["features"].append({'geometry': json.loads(ba.geom.geojson),
                                            'properties': properties,
                                            'type': "Feature",
                                            'id': ba.id,
                                            })
            except AttributeError: # no geom
                continue
            
        # strip non-json characters
        context['geojson'] = json.dumps(geojson).replace('\\','')

        # return
        return context
        