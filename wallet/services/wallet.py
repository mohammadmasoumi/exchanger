import abc
import logging
from typing import Dict, Any
from django.utils.translation import gettext_lazy as _
from wallet.models import Wallet, Currency
from wallet.exceptions import InvalidAmountError, InsufficientBalanceError
from wallet.utils import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


class WalletServiceAbstract(abc.ABC):
    @abc.abstractstaticmethod
    def withdraw(*, user: User, currency: Currency, amount: float) -> Dict[str, Any]:
        pass

    @abc.abstractstaticmethod
    def deposit(*, user: User, currency: Currency, amount: float) -> Dict[str, Any]:
        pass


class WalletService(WalletServiceAbstract):
    def __init__(self):
        pass

    @staticmethod
    def withdraw(*, user: User, currency: Currency, amount: float) -> Dict[str, Any]:
        """
        Withdraw amount from user's wallet
        :param user:
        :param currency:
        :param amount:
        :return:
        """
        try:
            wallet = Wallet.objects.withdraw(
                user=user, currency=currency, amount=amount
            )
        except InvalidAmountError:
            logger.error(
                f"Withdraw amount must be positive. curr: {currency} - amount: {amount}"
            )
            return {"success": False, "error": _("Withdraw amount must be positive")}
        except InsufficientBalanceError:
            logger.error(f"Insufficient balance. curr: {currency} - amount: {amount}")
            return {"success": False, "error": _("Insufficient balance")}
        except Exception as e:  # noqa
            logger.error(f"An error occurred. curr: {currency} - amount: {amount} - e: {e}")
            return {"success": False, "error": _("An error occurred")}

        return {"success": True, "wallet": wallet}

    @staticmethod
    def deposit(*, user: User, currency: Currency, amount: float) -> Dict[str, Any]:
        """
        Deposit amount to user's wallet
        :param user:
        :param currency:
        :param amount:
        :return:
        """
        try:
            wallet = Wallet.objects.deposit(user=user, currency=currency, amount=amount)
        except InvalidAmountError:
            logger.error(
                f"Withdraw amount must be positive. curr: {currency} - amount: {amount}"
            )
            return {"success": False, "error": _("Withdraw amount must be positive")}
        except Exception as e:  # noqa
            logger.error(f"An error occurred. curr: {currency} - amount: {amount} - e: {e}")
            return {"success": False, "error": _("An error occurred")}

        return {"success": True, "wallet": wallet}
