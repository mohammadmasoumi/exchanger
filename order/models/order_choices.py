from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    PENDING = "pending", _("Pending")
    COMPLETED = "completed", _("Completed")
    CANCELED = "canceled", _("Canceled")


class OrderSettlementStatus(models.TextChoices):
    UNAGGREGATED = "unaggregated", _("Unaggregated")
    PENDING = "pending", _("Pending")
    AGGREGATED = "aggregated", _("Aggregated")
    SUBMITTED = "submitted", _("Submitted")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")


class OrderSide(models.TextChoices):
    BUY = "buy", _("Buy")
    SELL = "sell", _("Sell")


class SettledOrderStatus(models.TextChoices):
    AGGREGATING = "aggregating", _("Aggregating")
    PENDING = "pending", _("Pending")
    SUBMITTED = "submitted", _("Submitted")
    FAILED = "failed", _("Failed")
    CANCELED = "canceled", _("Canceled")
