from django.core.management.base import BaseCommand
from wallet.models import Currency

CURRENCIES = {"USD": "United States Dollar", "ABAN": "AbanTether Coin"}


class Command(BaseCommand):
    help = "Init currency data"

    def handle(self, *args, **options):
        for code, descriptions in CURRENCIES.items():
            curr = Currency.objects.create(
                code=code, name=code, descriptions=descriptions
            )
            self.stdout.write(
                self.style.SUCCESS(f"Currency {curr.code} created successfully")
            )

        self.stdout.write(
            self.style.SUCCESS("Currency data synced and saved successfully")
        )
