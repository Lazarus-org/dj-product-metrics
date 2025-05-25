from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg
from product_metrics.models import Product
from product_metrics.mixins.admin.base import BaseModelAdmin
from product_metrics.settings.conf import config


@admin.register(Product, site=config.admin_site_class)
class ProductAdmin(BaseModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at", "average_rating")
    search_fields = ("name", "description")
    list_filter = ("is_active", "created_at", "updated_at")
    actions = ["activate_products", "deactivate_products"]
    fieldsets = (
        (None, {"fields": ("name", "description", "is_active")}),
        (
            _("Timestamps"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
    readonly_fields = ("created_at", "updated_at")

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(avg_rating=Avg("customer_feedback__rating"))
        )

    def average_rating(self, obj):
        if obj.avg_rating is None:
            return _("No ratings")
        return f"{obj.avg_rating:.1f}/5.0"

    average_rating.short_description = _("Average Rating")

    def activate_products(self, request, queryset):
        queryset.update(is_active=True)

    activate_products.short_description = _("Activate selected products")

    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)

    deactivate_products.short_description = _("Deactivate selected products")
