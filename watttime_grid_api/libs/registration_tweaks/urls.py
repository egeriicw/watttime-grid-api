from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

# See https://bitbucket.org/ubernostrum/django-registration/pull-request/63/django-16-compatibility-fix-auth-views/diff
# and http://stackoverflow.com/questions/19985103/django-1-6-and-django-registration-built-in-authentication-views-not-picked-up

urlpatterns = patterns('',

    # override the default urls
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': reverse_lazy('home')},
        name='auth_logout'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_done')},
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},
        name='password_reset_confirm'),

    # and now add the registration urls
    url(r'', include('registration.backends.default.urls')),
)