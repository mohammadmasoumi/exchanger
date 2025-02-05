from rest_framework import viewsets
from rest_framework.viewsets import mixins
from django.db import transaction

from order.authentications import MockBasicAuthentication
from order.tasks import aggregate_order, submit_order
from order.viewsets import container
from order.models import SettledOrder
from order.models.order_choices import OrderSide, SettledOrderStatus
from order.serializers import OrderCreateSerializer
from order.settings import order_settings


class DepositOrderViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = OrderCreateSerializer
    permission_classes = order_settings.DEFAULT_PERMISSION_CLASSES
    authentication_classes = (MockBasicAuthentication, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wallet_service = container.wallet_service()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        context["side"] = OrderSide.BUY
        return context

    def perform_create(self, serializer):
        with transaction.atomic():
            # Deposit the amount to the user's wallet
            self.wallet_service.deposit(
                user=self.request.user,
                currency=serializer.validated_data["currency"],
                amount=serializer.validated_data["amount"],
            )
            # Save the order
            order = serializer.save()
            if order.price > order_settings.AGGREGATION_THRESHOLD:
                settled_order = SettledOrder.objects.create(
                    currency=serializer.validated_data["currency"],
                    status=SettledOrderStatus.PENDING,
                    amount=order.amount,
                    price=order.price,
                )
                settled_order.orders.add(order)
                submit_order.apply_async(args=[settled_order.settled_id])
            else:
                aggregate_order.apply_async(args=[order.order_id])

            return order
