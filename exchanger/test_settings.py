from .settings import *  # noqa

CELERY_ALWAYS_EAGER = True

ORDER_SETTINGS = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "order.authentications.MockBasicAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated"
    ),
    "CURRENCY_MODEL": "wallet.Currency",
    "WALLET_MODEL": "wallet.Wallet",
    "CURRENCY_SERVICE": "wallet.services.CurrencyService",
    "WALLET_SERVICE": "wallet.services.WalletService",
}
