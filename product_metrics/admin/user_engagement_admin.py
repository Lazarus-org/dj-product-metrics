from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from product_metrics.models import UserEngagement
from product_metrics.mixins.admin.base import BaseModelAdmin
from product_metrics.settings.conf import config


@admin.register(UserEngagement, site=config.admin_site_class)
class UserEngagementAdmin(BaseModelAdmin):
    list_display = ("product", "date", "active_users", "churn_rate_color")
    autocomplete_fields = ("product",)
    search_fields = ("product__name", "date")
    list_filter = ("product", "date")
    date_hierarchy = "date"
    fieldsets = ((None, {"fields": ("product", "date", "active_users", "churn_rate")}),)

    def churn_rate_color(self, obj):
        if obj.churn_rate > 10:
            color = "red"
        elif obj.churn_rate > 5:
            color = "orange"
        else:
            color = "green"
        return format_html(
            '<span style="color: {};">{}%</span>',
            color,
            round(float(obj.churn_rate), 2),
        )

    churn_rate_color.short_description = _("Churn Rate")
