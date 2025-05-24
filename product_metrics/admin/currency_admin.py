from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from product_metrics.models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)
