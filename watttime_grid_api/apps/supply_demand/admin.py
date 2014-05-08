from django.contrib import admin
from apps.supply_demand.models import Load, TieFlow

admin.site.register(Load)
admin.site.register(TieFlow)
