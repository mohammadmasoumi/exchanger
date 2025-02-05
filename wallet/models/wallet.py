import uuid
from django.conf import settings
from django.db import models
from django.core import validators
from django.utils.translation import gettext_lazy as _
from wallet.models.managers import WalletManager


class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_(
            "The user that owns the wallet. The wallet is created for the user."
        ),
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text=_(
            "The balance of the wallet. It should be greater than or equal to 0."
        ),
        validators=[
            validators.MinValueValidator(
                0, message=_("Value must be greater than or equal to 0.")
            )
        ],
    )
    currency = models.ForeignKey(
        "Currency",
        on_delete=models.CASCADE,
    )

    objects = WalletManager()

    class Meta:
        unique_together = (
            "user",
            "currency",
        )  # Ensure one wallet per user per currency

    def __str__(self):
        return f"{self.user} - {self.currency} - {self.balance}"
