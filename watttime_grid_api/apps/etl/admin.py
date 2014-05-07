from django.contrib import admin
from apps.etl.models import ETLJob


class ETLJobAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('id', 'created_at', 'task', 'args', 'kwargs', 'success')
    list_filter = ('task', 'success', 'args', 'kwargs')
    exclude = ('datapoints',)
    readonly_fields = ('datapoints_admin_links', 'gen_admin_links', 'carbon_admin_links', 'moer_admin_links',
        'task', 'args', 'kwargs', 'errors', 'created_at')


admin.site.register(ETLJob, ETLJobAdmin)
