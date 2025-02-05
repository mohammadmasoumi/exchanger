class WalletError(Exception):
    """Base exception for wallet-related errors."""

    pass


class InsufficientBalanceError(WalletError):
    """Raised when balance is insufficient."""

    pass


class CurrencyNotFoundError(WalletError):
    """Raised when currency does not exist."""

    pass


class WalletNotFoundError(WalletError):
    """Raised when a user does not have a wallet."""

    pass


class InvalidAmountError(WalletError):
    """Raised when an amount is zero or negative."""

    pass
