from django.contrib import admin
from apps.griddata.models import DataPoint, DataSeries

admin.site.register(DataPoint)
admin.site.register(DataSeries)
