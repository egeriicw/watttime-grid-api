from django.views.generic.detail import DetailView
from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import response, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views as authtoken_views
from .models import reset_auth_token


class ObtainAuthToken(authtoken_views.ObtainAuthToken):
    """
    API endpoint that retreives an API token.
    username -- Username for an existing user account.
    password -- Password for an existing user account.
    """
    pass


class ResetAuthToken(authtoken_views.ObtainAuthToken):
    """
    API endpoint that resets an API token and retrieves the new token.
    username -- Username for an existing user account.
    password -- Password for an existing user account.
    """
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            # and create new one
            token, created = reset_auth_token(serializer.object['user'])

            # return
            return response.Response({'token': token.key, 'reset_success': created})

        # invalid serializer
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(DetailView):
    """View to retrieve a user's token"""
    model = Token

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenView, self).dispatch(*args, **kwargs)

    def get_object(self):
        """get the token associated with the user"""
        token = get_object_or_404(Token, user=self.request.user)
        return token


class TokenReset(View):
    """View to reset a user's token. Only POST allowed."""

    # only allow post
    http_method_names = ['post']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenReset, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        token, created = reset_auth_token(request.user)
        return redirect(reverse_lazy('token-detail'))
