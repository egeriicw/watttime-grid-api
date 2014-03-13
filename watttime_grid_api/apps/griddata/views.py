from django.views.generic import TemplateView
from django.db.models import Sum
from apps.griddata.models import DataSeries, DataPoint
import json
from datetime import datetime
import pytz
import copy


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
        

class DashboardView(TemplateView):
    def get_context_data(self, **kwargs):
        # get other context
        context = super(DashboardView, self).get_context_data(**kwargs)
        
        # set up storage
        data = []
        
        # get dates truncated to hour
        datehrs = DataPoint.objects.datetimes('timestamp', 'hour')
        
        # fields that should be distinct
        distinct_fields = ('ba', 'market')
        filters = DataPoint.objects.order_by(*distinct_fields).values(*distinct_fields).distinct()
        
        # loop over start of time ranges
        for its in range(len(datehrs)-1):
            # collect data points in time range
            dps_at_time = DataPoint.objects.filter(timestamp__gte=datehrs[its],
                                                   timestamp__lt=datehrs[its+1])
                                                   
            # apply other filters
            for filterset in filters:
                # filter data
                dps_in_filter = dps_at_time.filter(**filterset)
                
                # calculate and add to storage
                this_data = copy.deepcopy(filterset)
                this_data.update({'timestamp': datehrs[its],
                                  'n_obs': dps_in_filter.count(),
                                })
                this_data.update(dps_in_filter.aggregate(total_gen=Sum('genmix__gen_MW')))
                data.append(this_data)
            
        # return
        context['data'] = data
        return context
