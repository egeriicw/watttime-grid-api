from django.contrib import admin
from apps.gridentities.models import BalancingAuthority, FuelType

admin.site.register(BalancingAuthority)
admin.site.register(FuelType)
