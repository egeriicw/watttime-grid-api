from django.contrib import admin
from apps.carbon.models import Carbon, FuelCarbonIntensity

admin.site.register(Carbon)
admin.site.register(FuelCarbonIntensity)
