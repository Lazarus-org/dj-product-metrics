from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProductMetricsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "product_metrics"
    verbose_name = _("Django Product Metrics")
    
