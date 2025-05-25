from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from product_metrics.models import Currency
from product_metrics.mixins.admin.base import BaseModelAdmin
from product_metrics.settings.conf import config


@admin.register(Currency, site=config.admin_site_class)
class CurrencyAdmin(BaseModelAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("code",)
