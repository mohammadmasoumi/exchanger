from django.db import models, transaction
from django.db.models import F

from wallet.exceptions import InvalidAmountError, InsufficientBalanceError


class WalletManager(models.Manager):
    @transaction.atomic
    def deposit(self, *, user, currency, amount):
        """Thread-safe deposit operation"""
        if amount <= 0:
            raise InvalidAmountError
            # raise ValueError(_("Deposit amount must be positive"))

        self.get_or_create(user=user, currency=currency, defaults={"balance": 0})
        wallet = self.select_for_update().get(user=user, currency=currency)

        wallet.balance = F("balance") + amount
        wallet.save(update_fields=["balance"])

        # Transaction.objects.create(user=user, currency=currency, transaction_type='deposit', amount=amount)
        return wallet

    @transaction.atomic
    def withdraw(self, *, user, currency, amount):
        """Thread-safe withdraw operation"""
        if amount <= 0:
            raise InvalidAmountError
            # raise ValueError(_("Withdraw amount must be positive"))

        wallet = self.select_for_update().get(user=user, currency=currency)

        if wallet.balance < amount:
            raise InsufficientBalanceError
            # raise ValueError(_("Insufficient balance"))

        wallet.balance = F("balance") - amount
        wallet.save(update_fields=["balance"])

        # Transaction.objects.create(user=user, currency=currency, transaction_type='withdraw', amount=amount)
        return wallet
