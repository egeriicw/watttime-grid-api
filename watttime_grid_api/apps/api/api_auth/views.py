from django.views.generic import DetailView
from rest_framework import response, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken import views as authtoken_views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


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
            # delete existing token
            Token.objects.filter(user=serializer.object['user']).delete()

            # and create new one
            token, created = Token.objects.get_or_create(user=serializer.object['user'])

            # return
            return response.Response({'token': token.key, 'reset_success': created})

        # invalid serializer
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(DetailView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TokenView, self).dispatch(*args, **kwargs)

    def get_object(self):
        token, created = Token.objects.get_or_create(user=self.request.user)
        return token
