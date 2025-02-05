from django.db import models
from django.core.cache import cache


class CurrencyManager(models.Manager):
    CACHE_KEY = "currency_{code}"

    def from_cache(self, *, code):
        """
        Retrieve an object by its code from the cache.
        """

        key = self.CACHE_KEY.format(code=code)
        currency = cache.get(key)

        if currency is None:
            currency = self.get(code=code)
            cache.set(key, currency)

        return currency

    def clear_cache(self, *, code):
        """
        Clear the cache for a specific currency object by its code.
        """
        key = self.CACHE_KEY.format(code=code)
        cache.delete(key)
