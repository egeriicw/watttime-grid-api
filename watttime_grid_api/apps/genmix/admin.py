from django.contrib import admin
from apps.genmix.models import DataPoint, DataSeries, Generation

admin.site.register(DataPoint)
admin.site.register(DataSeries)
admin.site.register(Generation)
