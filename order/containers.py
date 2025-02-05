# myapp/containers.py
import logging

from dependency_injector import containers, providers
from order.settings import order_settings

logger = logging.getLogger(__name__)


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container"""

    logger.info(" - Creating Order Container")

    wallet_service = providers.Singleton(order_settings.WALLET_SERVICE)
    currency_service = providers.Singleton(order_settings.CURRENCY_SERVICE)
