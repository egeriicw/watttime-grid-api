from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


class ProfileView(DetailView):
    """View to retrieve a user's profile"""
    model = User

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)

    def get_object(self):
        """get the user"""
        return self.request.user
