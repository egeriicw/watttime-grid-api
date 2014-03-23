from django.conf.urls import patterns, include, url
from .views import ProfileView

urlpatterns = patterns('',
    url(r'^$', ProfileView.as_view(template_name="accounts/profile.html"), name='profile'),
)