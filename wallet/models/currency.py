from django.db import models
from django.utils.translation import gettext_lazy as _
from wallet.models.managers import CurrencyManager


class Currency(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    descriptions = models.TextField(
        blank=True, null=True, help_text=_("Description of the currency.")
    )

    objects = CurrencyManager()

    def __str__(self):
        return self.code
