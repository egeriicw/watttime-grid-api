from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from apps.gridentities.models import BalancingAuthority, FuelType, PowerPlant

admin.site.register(BalancingAuthority)
admin.site.register(FuelType)
geoadmin.site.register(PowerPlant)