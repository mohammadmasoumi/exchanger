from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

MOCK_PHONE_NUMBER = "1234567890"


class MockBasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            user = get_user_model().objects.get(phone_number=MOCK_PHONE_NUMBER)
        except get_user_model().DoesNotExist:
            user = get_user_model().objects.create_user(phone_number=MOCK_PHONE_NUMBER)
            # raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

        return user, None  # Return user and None for the auth token

    def authenticate_header(self, request):
        return "Basic"
