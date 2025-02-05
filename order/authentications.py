import base64

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class MockBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            # Get user
            user = (
                get_user_model().objects.get(phone_number="1234567890")
            )

        except get_user_model().DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user, None  # Return user and None for the auth token

    def authenticate_header(self, request):
        return "Basic"
