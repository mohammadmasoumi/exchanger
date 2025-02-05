from decimal import Decimal
from django.conf import settings
from django.test.signals import setting_changed
from django.utils.translation import gettext_lazy as _

from typing import Dict, Any
from django.utils.module_loading import import_string

APP_SETTINGS = "ORDER_SETTINGS"

DEFAULTS: Dict[str, Any] = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    # Define the minimum amount required for aggregation per currency
    "AGGREGATION_THRESHOLD": Decimal("10.00"),
    "CURRENCY_MODEL": "",
    "WALLET_MODEL": "",
    "WALLET_SERVICE": "",
    "CURRENCY_SERVICE": "",
}

IMPORT_STRINGS = (
    "DEFAULT_PERMISSION_CLASSES",
    "WALLET_SERVICE",
    "CURRENCY_SERVICE"
)


def perform_import(val, setting_name):
    """
    If the given setting is a string import notation,
    then perform the necessary import or imports.
    """
    if val is None:
        return None
    elif isinstance(val, str):
        return import_from_string(val, setting_name)
    elif isinstance(val, (list, tuple)):
        return [import_from_string(item, setting_name) for item in val]
    return val


def import_from_string(val, setting_name):
    """
    Attempt to import a class from a string representation.
    """
    try:
        return import_string(val)
    except ImportError as e:
        msg = _(f"Could not import '%s' for {APP_SETTINGS} '{val}'. {e.__class__.__name__}: {e}.")
        raise ImportError(msg)


class APISettings:
    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = user_settings
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, APP_SETTINGS, {})
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(_(f"Invalid {APP_SETTINGS} setting: '{attr}'"))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Coerce import strings into classes
        if attr in self.import_strings:
            val = perform_import(val, attr)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


order_settings = APISettings(user_settings=None,defaults=DEFAULTS)


def reload_api_settings(*args, **kwargs):
    setting = kwargs['setting']
    if setting == APP_SETTINGS:
        order_settings.reload()


setting_changed.connect(reload_api_settings)
