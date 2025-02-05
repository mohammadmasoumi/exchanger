from django.contrib import admin
from order.models import Order, SettledOrder


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "user", "amount", "status", "settlement_status", "created_at")  # Columns in list view
    list_filter = ("status", "created_at")  # Filter sidebar
    search_fields = ("order_id", "user__username")  # Search bar
    ordering = ("-created_at",)  # Default sorting


@admin.register(SettledOrder)
class SettledOrderAdmin(admin.ModelAdmin):
    list_display = ("settled_id", "currency", "amount", "status", "external_wallet", "created_at")
    search_fields = ("settled_id", "currency__code")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)

    # Best way to represent ManyToManyField
    filter_horizontal = ("orders",)  # Adds a nice UI for selecting related orders
