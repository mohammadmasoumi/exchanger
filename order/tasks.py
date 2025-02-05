import logging

from celery import shared_task
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from order.settings import order_settings
from order.services import submit_to_external_exchange
from order.models import Order, SettledOrder
from order.models.order_choices import (
    OrderSide,
    OrderStatus,
    OrderSettlementStatus,
    SettledOrderStatus,
)

logger = logging.getLogger(__name__)


@shared_task
def aggregate_order(order_id: str):
    """
    Groups pending orders by currency, aggregates them, and submits to external API
    if the total per currency exceeds the threshold.
    """

    def get_currency(order: Order):
        match order.side:
            case OrderSide.BUY:
                curr = order.target_currency
            case OrderSide.SELL:
                curr = order.source_currency
            case _:
                logger.error(f"Invalid order side for order {order_id}.")
                raise ValueError(_("Invalid order side."))

        return curr

    with transaction.atomic():
        # Retrieve order
        try:
            unaggregated_order = Order.objects.select_for_update().get(
                order_id=order_id,
                status=OrderStatus.COMPLETED,
                settlement_status=OrderSettlementStatus.UNAGGREGATED,
            )
        except Order.DoesNotExist:
            logger.error(f"Order {order_id} not found for aggregation.")
            raise Order.DoesNotExist(f"Order {order_id} not found for aggregation.")

        currency_to_settle = get_currency(unaggregated_order)

        # Update the order status to prevent double aggregation
        settled_orders = (
            SettledOrder.objects.prefech_related("orders")
            .filter(
                currency=currency_to_settle,
                status=SettledOrderStatus.AGGREGATING,
            )
            .select_for_update()
        )

        # If no settled orders exist, create a new one
        if not settled_orders.exists():
            settled_order = SettledOrder.objects.create(
                currency=currency_to_settle,
                status=SettledOrderStatus.AGGREGATING,
                amount=unaggregated_order.amount,
                price=unaggregated_order.price,
            )
            settled_order.orders.add(unaggregated_order)
        else:
            # Merge all orders into the first one (you can change the logic here if needed)
            settled_order = (
                settled_orders.first()
            )  # Pick the first one to aggregate into

            # Sum up amounts and prices from all the aggregated orders
            for settled_order_item in settled_orders[1:]:
                settled_order.amount += settled_order_item.amount
                settled_order.price += settled_order_item.price
                settled_order.orders.add(
                    *settled_order_item.orders.all()
                )  # Add related orders

            # Delete redundant settled orders (those that were merged)
            for order in settled_orders.exclude(id=settled_order.id):
                order.delete()

            # Add the unaggregated order to the merged settled order
            settled_order.amount += unaggregated_order.amount
            settled_order.price += unaggregated_order.price
            settled_order.orders.add(
                unaggregated_order
            )  # Add the unaggregated order to the merged orders

            # Update the unaggregated order
            unaggregated_order.settlement_status = OrderSettlementStatus.AGGREGATED
            unaggregated_order.save(update_fields=["settlement_status"])

            if settled_order.price >= order_settings.AGGREGATION_THRESHOLD:
                settled_order.status = SettledOrderStatus.PENDING
                settled_order.save(update_fields=["amount", "price", "status"])

                # Call the external API to submit the batch
                submit_order.delay(settled_order.settled_id)
            else:
                # Save the merged settled order
                settled_order.save(update_fields=["amount", "price"])

    logger.info(f"Aggregated order {order_id} into {settled_order.settled_id}.")


@shared_task
def submit_order(settled_id: str):
    with transaction.atomic():
        # Lock the main settled order
        settled_order = (
            SettledOrder.objects.select_for_update()
            .prefetch_related("orders")
            .get(settled_id=settled_id)
        )

        # Fetch orders only once and store in a list
        orders = list(settled_order.orders.all())

        # Submit to external exchange
        response = submit_to_external_exchange(settled_order)

        if response.success:
            # Update all orders' settlement status in bulk
            for order in orders:
                order.settlement_status = OrderSettlementStatus.SUBMITTED
            Order.objects.bulk_update(orders, ["settlement_status"])

            # Update settled order
            settled_order.status = SettledOrderStatus.SUBMITTED
            settled_order.external_wallet = response.transaction_id
            settled_order.save(update_fields=["status", "external_wallet"])
        else:
            # Update all orders' settlement status in bulk for failure case
            for order in orders:
                order.settlement_status = OrderSettlementStatus.FAILED
            Order.objects.bulk_update(orders, ["settlement_status"])

            # Update settled order status
            settled_order.status = SettledOrderStatus.FAILED
            settled_order.save(update_fields=["status"])

    logger.info(f"Submitted order {settled_id} to external exchange.")
