from django.urls import path, include
from order.routers import router

urlpatterns = [
    path("", include(router.urls)),
]
