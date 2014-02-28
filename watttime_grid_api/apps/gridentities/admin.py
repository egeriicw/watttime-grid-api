from django.contrib.gis import admin
from apps.gridentities.models import BalancingAuthority, FuelType, PowerPlant, ServiceArea

admin.site.register(BalancingAuthority)
admin.site.register(FuelType)
admin.site.register(PowerPlant)
admin.site.register(ServiceArea)
