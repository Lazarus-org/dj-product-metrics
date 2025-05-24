from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from product_metrics.models import CustomerFeedback


@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ("product", "date", "rating", "rating_stars", "feedback_preview")
    autocomplete_fields = ("product",)
    search_fields = ("product__name", "date", "feedback")
    list_filter = ("product", "date", "rating")
    date_hierarchy = "date"
    fieldsets = ((None, {"fields": ("product", "date", "rating", "feedback")}),)

    def rating_stars(self, obj):
        stars = "★" * int(obj.rating) + "☆" * (5 - int(obj.rating))
        return format_html('<span style="color: gold;">{}</span>', stars)

    rating_stars.short_description = _("Rating")

    def feedback_preview(self, obj):
        if obj.feedback:
            return obj.feedback[:32] + "..." if len(obj.feedback) > 32 else obj.feedback
        return "-"

    feedback_preview.short_description = _("Feedback Preview")
