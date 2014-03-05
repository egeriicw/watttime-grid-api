from django.contrib.gis import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # home
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),

    # api
    url(r'^api/v1/', include('apps.api.urls')),

    # api docs
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
