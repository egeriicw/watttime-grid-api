from django.contrib.gis import admin
from apps.gridentities.models import BalancingAuthority, FuelType, PowerPlant

admin.site.register(BalancingAuthority)
admin.site.register(FuelType)
admin.site.register(PowerPlant)
