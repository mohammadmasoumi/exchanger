from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def _get_model(model_path, error_message):
    try:
        return django_apps.get_model(model_path, require_ready=False)
    except (ValueError, LookupError):
        raise ImproperlyConfigured(error_message)


def get_user_model():
    """
    Return the Order model that is active in this project.
    """
    return _get_model(
        settings.AUTH_USER_MODEL,
        "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        " or refers to a model that has not been installed",
    )
