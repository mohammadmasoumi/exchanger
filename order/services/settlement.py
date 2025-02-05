import uuid
import logging
from order.services.types import MockExchangerResponse
from order.models import SettledOrder


def submit_to_external_exchange(settle_order: SettledOrder) -> MockExchangerResponse:
    logging.info(f"{settle_order} submitted to external exchange.")
    return MockExchangerResponse(transaction_id=uuid.uuid4().hex, success=True)
