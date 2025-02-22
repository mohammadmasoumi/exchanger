from unittest.mock import patch, MagicMock
from django.db import transaction
from django.urls import reverse
from django.test.utils import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
# from order.models import SettledOrder, Order
# from order.serializers import OrderCreateSerializer
# from order.models.order_choices import OrderSide, SettledOrderStatus
# from order.settings import order_settings


@override_settings(AUTH_USER_MODEL="account.User")
class DepositOrderViewSetTest(APITestCase):
    def setUp(self):
        from django.conf import settings
        print(settings.DJANGO_SETTINGS_MODULE)

    @patch("order.tasks.aggregate_order.apply_async")
    @patch("order.tasks.submit_order.apply_async")
    def test_perform_create_below_threshold(
        self, mock_submit_order, mock_aggregate_order
    ):
        data = {
            "currency": "USD",
            "amount": 100,
        }
        response = self.client.post(reverse("deposit-order"), data)
        print(response.json())
        # Assert
        # self.viewset.wallet_service.deposit.assert_called_once_with(
        #     user=self.user, currency=order_data["currency"], amount=order_data["amount"]
        # )
        # mock_aggregate_order.assert_called_once()
        # mock_submit_order.assert_not_called()

    # @patch("order.tasks.aggregate_order.apply_async")
    # @patch("order.tasks.submit_order.apply_async")
    # def test_perform_create_above_threshold(
    #     self, mock_submit_order, mock_aggregate_order
    # ):
    #     # Arrange
    #     order_data = {
    #         "currency": "ABAN",
    #         "amount": 100,
    #     }
    #     serializer = OrderCreateSerializer(data=order_data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     # Act
    #     with transaction.atomic():
    #         self.viewset.perform_create(serializer)
    #
    #     # Assert
    #     self.viewset.wallet_service.deposit.assert_called_once_with(
    #         user=self.user, currency=order_data["currency"], amount=order_data["amount"]
    #     )
    #     mock_submit_order.assert_called_once()
    #     mock_aggregate_order.assert_not_called()
    #
    #     settled_order = SettledOrder.objects.first()
    #     self.assertIsNotNone(settled_order)
    #     self.assertEqual(settled_order.status, SettledOrderStatus.PENDING)
    #     self.assertEqual(settled_order.currency, order_data["currency"])
    #     self.assertEqual(settled_order.amount, order_data["amount"])
    #     self.assertEqual(settled_order.price, order_data["price"])
    #
    # def test_get_serializer_context(self):
    #     # Arrange
    #     self.viewset.request = MagicMock(user=self.user)
    #
    #     # Act
    #     context = self.viewset.get_serializer_context()
    #
    #     # Assert
    #     self.assertEqual(context["user"], self.user)
    #     self.assertEqual(context["side"], OrderSide.BUY)
