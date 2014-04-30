from django.contrib import admin
from apps.marginal.models import StructuralModelSet, SimpleStructuralModel, MOERAlgorithm, MOER

class StructuralModelInline(admin.TabularInline):
    model = SimpleStructuralModel


class StructuralModelSetAdmin(admin.ModelAdmin):
	inlines = [StructuralModelInline]


admin.site.register(StructuralModelSet, StructuralModelSetAdmin)
admin.site.register(SimpleStructuralModel)
admin.site.register(MOERAlgorithm)
admin.site.register(MOER)