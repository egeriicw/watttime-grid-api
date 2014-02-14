from django.contrib import admin
from apps.gridentities.models import BalancingAuthority, GenType

admin.site.register(BalancingAuthority)
admin.site.register(GenType)
