from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    """
    A model representing currencies.

    Attributes:
        code (str): ISO 4217 currency code (e.g., USD, IRR)
        name (str): Full name of the currency
    """

    code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_("Currency Code"),
        help_text=_("ISO 4217 currency code (e.g., USD, IRR)."),
        db_comment="Stores the ISO 4217 currency code.",
    )
    name = models.CharField(
        max_length=50,
        verbose_name=_("Currency Name"),
        help_text=_("Full name of the currency (e.g., US Dollar)."),
        db_comment="Stores the full name of the currency.",
    )

    class Meta:
        db_table_comment = "Stores currency information."
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.name} ({self.code})"
