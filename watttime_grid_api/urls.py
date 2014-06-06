from django.contrib.gis import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView


# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Admin panel, documentation, tools:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin_tools/', include('admin_tools.urls')),

    # home
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    url(r'^faq[/]$', TemplateView.as_view(template_name="faq.html"), name='faq'),
    url(r'^contact[/]$', TemplateView.as_view(template_name="contact.html"), name='contact'),
    url(r'^dashboard[/]$', TemplateView.as_view(template_name="dashboard.html"), name='dashboard'),
    
    # griddata dashboard views
    url(r'', include('apps.griddata.urls')),

    # api
    url(r'^api/v1/', include('apps.api.urls')),
    url(r'^api/', RedirectView.as_view(url='/api/v1/')),

    # api docs
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # api tokens
    url(r'^accounts/token/', include('apps.api.api_auth.urls')),

    # registration
    url(r'^accounts/', include('libs.registration_tweaks.urls')),

    # profile
    url(r'^accounts/profile/', include('apps.accounts.urls')),
)
