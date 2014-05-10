from django.views.generic import TemplateView
from django.db.models import Sum
from apps.griddata.models import DataSeries, DataPoint
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
            # set up defaults
            carbon_val = 0
            td = None
            lag_units = 'minutes'

            try:
                # get most recent data
                dp = ds.datapoints.latest()
                carbon_val = round(dp.carbon.emissions_intensity, 0)
                td = round((pytz.utc.localize(datetime.utcnow()) - dp.timestamp).total_seconds() / 60, 0)

                if td > 60 * 24:
                    # stale data greater than 1 day old
                    carbon_val = 0
                    td /= 60*24
                    lag_units = 'days'

            except:
                # use defaults
                pass

            try:
                # set up for content
                ba = ds.ba
                properties = {'name': str(ba),
                              'carbon': carbon_val,
                              'lag': td,
                              'lag_units': lag_units,
                              }
                geojson["features"].append({'geometry': json.loads(ba.geom.geojson),
                                            'properties': properties,
                                            'type': "Feature",
                                            'id': ba.id,
                                            })
            except AttributeError:
                # no geom
                continue
            
        # strip non-json characters
        context['geojson'] = json.dumps(geojson).replace('\\','')

        # return
        return context
        