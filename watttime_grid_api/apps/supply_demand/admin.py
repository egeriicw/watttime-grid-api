from django.contrib import admin
from apps.supply_demand.models import Load, TieFlow, Generation

class LoadAdmin(admin.ModelAdmin):
	list_display = ('id', 'dp', 'value', 'units')


class TieFlowAdmin(admin.ModelAdmin):
	list_display = ('id', 'dp_source', 'dp_dest', 'value', 'units')


class GenerationAdmin(admin.ModelAdmin):
	list_display = ('id', 'mix', 'fuel', 'gen_MW')


admin.site.register(Load, LoadAdmin)
admin.site.register(TieFlow, TieFlowAdmin)
admin.site.register(Generation, GenerationAdmin)
