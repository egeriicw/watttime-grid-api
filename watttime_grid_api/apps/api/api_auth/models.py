from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    # from http://www.django-rest-framework.org/api-guide/authentication#tokenauthentication
    if created:
        token, tcreated = Token.objects.get_or_create(user=instance)

def reset_auth_token(user):
    """Resets a user's auth token, and returns new token and success boolean"""
    # delete existing token
    Token.objects.filter(user=user).delete()

    # and create new one
    token, created = Token.objects.get_or_create(user=user)

    # return
    return token, created
