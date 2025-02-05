import logging

from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from order.models import Order
from order.models.order_choices import OrderSide, OrderStatus
from order.utils import get_currency_model

logger = logging.getLogger(__name__)

Currency = get_currency_model()

# Constant price for currency conversion
BID_PRICE = 4  # dollar


class OrderCreateSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Order
        fields = ("currency", "amount")

    def validate_currency(self, currency: str) -> Currency:
        if not currency:
            raise serializers.ValidationError(_("Currency is required"))

        try:
            currency = Currency.objects.from_cache(code=currency)
        except Currency.DoesNotExist:
            raise serializers.ValidationError(_("Currency does not exist"))

        return currency

    def validate_amount(self, amount: float) -> float:
        if amount <= 0:
            raise serializers.ValidationError(_("Amount must be greater than zero"))

        return amount

    def create(self, validated_data):
        validated_data["user"] = self.context["user"]
        validated_data["side"] = self.context["side"]
        validated_data["price"] = validated_data["amount"] * BID_PRICE
        validated_data["status"] = (
            OrderStatus.COMPLETED
        )  # Mark order as completed - Matched

        match validated_data["side"]:
            case OrderSide.BUY:
                validated_data["source_currency"] = Currency.objects.from_cache(
                    code="USD"
                )
                validated_data["target_currency"] = validated_data.pop("currency")
            case OrderSide.SELL:
                validated_data["source_currency"] = validated_data.pop("currency")
                validated_data["target_currency"] = Currency.objects.from_cache(
                    code="USD"
                )
            case _:
                raise ValueError(_("Invalid order side"))

        try:
            return Order.objects.create(**validated_data)
        except IntegrityError as e:
            logger.error(f"Order creation failed: {e}")
            raise serializers.ValidationError(_("Order creation failed"))
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise serializers.ValidationError(_("Unexpected error"))
