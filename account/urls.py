from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.viewsets import UserCreateView, LogoutView, LogoutAllView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="user-register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("logout/all/", LogoutAllView.as_view(), name="auth_logout_all"),
]
