from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from order.settings import order_settings


def _get_model(model_path, error_message):
    try:
        return django_apps.get_model(model_path, require_ready=False)
    except (ValueError, LookupError):
        raise ImproperlyConfigured(error_message)


def get_currency_model():
    """
    Return the Order model that is active in this project.
    """
    return _get_model(
        order_settings.CURRENCY_MODEL,
        "ORDER_MODEL must be of the form 'app_label.model_name'"
        " or refers to a model that has not been installed",
    )
