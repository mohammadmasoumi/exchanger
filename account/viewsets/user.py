from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from account.serializers import UserCreateSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """Register a new user"""

    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
