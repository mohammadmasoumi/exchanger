import abc
import logging
from typing import Dict, Any
from django.utils.translation import gettext_lazy as _
from wallet.models import Currency


logger = logging.getLogger(__name__)


class CurrencyServiceAbstract(abc.ABC):
    @abc.abstractstaticmethod
    def get_currency(*, code) -> Dict[str, Any]:
        pass


class CurrencyService:
    def __init__(self):
        pass

    @staticmethod
    def get_currency(*, code) -> Dict[str, Any]:
        try:
            currency = Currency.objects.from_cache(code=code)
            return {"success": True, "currency": currency}
        except Currency.DoesNotExist:
            logger.error(f"Currency not found. code: {code}")
            return {"success": False, "error": _("Currency not found")}
