from django.conf.urls import patterns, include, url
from .views import TokenView, TokenReset


urlpatterns = patterns('',
    url(r'^$',
        TokenView.as_view(template_name="api/api_auth/token.html"),
        name='token-detail'),
    url(r'^reset[/]$', TokenReset.as_view(), name='token-reset'),
)