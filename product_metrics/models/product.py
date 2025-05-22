from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """
    A model representing a product in the system.

    This model stores basic information about products including their name,
    description, and timestamps for creation and updates. It serves as the
    central entity for tracking various product metrics.

    Attributes:
        name (str): The name of the product
        description (str): A detailed description of the product
        created_at (datetime): Timestamp when the product was created
        updated_at (datetime): Timestamp when the product was last updated
        is_active (bool): Whether the product is currently active
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("Product Name"),
        help_text=_("The name of the product."),
        db_comment="Stores the name of the product.",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Product Description"),
        help_text=_("A brief description of the product."),
        db_comment="Stores a description of the product.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when the product was created."),
        db_comment="Stores the creation timestamp of the product.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when the product was last updated."),
        db_comment="Stores the last update timestamp of the product.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
        help_text=_("Whether the product is currently active."),
        db_comment="Indicates if the product is currently active in the system.",
    )

    class Meta:
        db_table_comment = "Stores information about products."
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name
