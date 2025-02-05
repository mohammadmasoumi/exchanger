from rest_framework.routers import DefaultRouter
from order.viewsets import DepositOrderViewSet

# Initialize the router
router = DefaultRouter(trailing_slash=True)
router.register("deposit", DepositOrderViewSet, basename="deposit-order")
