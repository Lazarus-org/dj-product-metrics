from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from product_metrics.models import SalesData


@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ("product", "date", "units_sold", "revenue", "revenue_per_unit")
    autocomplete_fields = ("product", "currency")
    search_fields = ("product__name", "date")
    list_filter = ("product", "date", "currency")
    date_hierarchy = "date"
    fieldsets = (
        (None, {"fields": ("product", "date", "units_sold", "revenue", "currency")}),
    )

    def revenue_per_unit(self, obj):
        if obj.units_sold > 0:
            return f"{obj.revenue / obj.units_sold:,.0f} {obj.currency.code}"
        return _("N/A")

    revenue_per_unit.short_description = _("Revenue per Unit")

    def revenue(self, obj):
        return f"{obj.revenue:,.0f} {obj.currency.code}"

    revenue.short_description = _("Revenue")
