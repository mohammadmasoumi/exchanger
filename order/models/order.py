import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core import validators
from order.settings import order_settings
from order.models.order_choices import (
    OrderStatus,
    OrderSide,
    OrderSettlementStatus,
    SettledOrderStatus,
)

DECIMAL_PRECISION = 8


class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False)
    # Keeps orders even if users are deleted, ensuring referential integrity.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,  # In case of user deletion
        blank=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    settlement_status = models.CharField(
        max_length=20,
        choices=OrderSettlementStatus.choices,
        default=OrderSettlementStatus.PENDING,
    )
    source_currency = models.ForeignKey(
        order_settings.CURRENCY_MODEL,
        on_delete=models.PROTECT,
        related_name="source_orders",
    )
    target_currency = models.ForeignKey(
        order_settings.CURRENCY_MODEL,
        on_delete=models.PROTECT,
        related_name="destination_orders",
    )
    amount = models.DecimalField(
        max_digits=18,
        decimal_places=DECIMAL_PRECISION,
        validators=[validators.MinValueValidator(Decimal("0.00000001"))],
    )
    price = models.DecimalField(
        max_digits=18,
        decimal_places=DECIMAL_PRECISION,
        validators=[validators.MinValueValidator(Decimal("0.00000001"))],
    )
    side = models.CharField(
        max_length=10, choices=OrderSide.choices, default=OrderSide.SELL
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, primary_key=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Ensures latest orders are fetched first

    def __str__(self):
        if self.side == OrderSide.BUY:
            curr_name = f"{self.source_currency} | {self.target_currency}"
        else:
            curr_name = f"{self.target_currency} | {self.source_currency}"

        return f"Order {self.order_id}: {self.side} {self.amount} ({curr_name}) at {self.price}"


class SettledOrder(models.Model):
    settled_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Many-to-many relationship to group orders together.
    orders = models.ManyToManyField(
        Order,
        related_name="settled_orders",
    )
    currency = models.ForeignKey(
        order_settings.CURRENCY_MODEL,
        on_delete=models.PROTECT,
        related_name="settled_orders",
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=DECIMAL_PRECISION,
        validators=[validators.MinValueValidator(Decimal("0.00000001"))],
    )
    price = models.DecimalField(
        max_digits=18,
        decimal_places=DECIMAL_PRECISION,
        validators=[validators.MinValueValidator(Decimal("0.00000001"))],
    )
    external_wallet = models.CharField(max_length=1024, blank=True, null=True)
    status = models.CharField(SettledOrderStatus, default=SettledOrderStatus.PENDING)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Settled Order {self.settled_id} ({self.status}) - Currency: {self.currency} - Total: {self.amount}"
