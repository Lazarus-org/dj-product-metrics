from django.contrib.admin import ModelAdmin

from product_metrics.mixins.admin.permission import AdminPermissionControlMixin


class BaseModelAdmin(AdminPermissionControlMixin, ModelAdmin):
    """Base class for all ModelAdmin classes in the Django admin interface.

    This class provides common functionalities that can be reused across
    different admin models, promoting consistency and reducing code duplication.


    Usage:
        Subclass `BaseModelAdmin` to create custom admin interfaces for your models,
        include the common configurations and functionalities based on the target ModelAdmin.

    """
