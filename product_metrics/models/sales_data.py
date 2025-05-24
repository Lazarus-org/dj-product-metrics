from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from product_metrics.models.product import Product
from product_metrics.models.currency import Currency


class SalesData(models.Model):
    """
    A model representing sales data for products.

    This model tracks daily sales metrics including units sold and revenue
    generated for each product. It helps in analyzing sales performance
    and trends over time.

    Attributes:
        product (Product): The associated product
        date (date): The date of the sales data
        units_sold (int): Number of units sold
        revenue (decimal): Revenue generated in the specified currency
        currency (Currency): The currency of the revenue
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales_data",
        verbose_name=_("Product"),
        help_text=_("The product associated with this sales data."),
        db_comment="Foreign key to the Product model.",
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("The date of the sales data."),
        db_comment="Stores the date of the sales data.",
        db_index=True,
    )
    units_sold = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_("Units Sold"),
        help_text=_("The number of units sold on this date."),
        db_comment="Stores the number of units sold.",
    )
    revenue = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Revenue"),
        help_text=_("The revenue generated on this date."),
        db_comment="Stores the revenue generated.",
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="sales_data",
        verbose_name=_("Currency"),
        help_text=_("The currency of the revenue."),
        db_comment="Foreign key to the Currency model.",
    )

    class Meta:
        db_table_comment = "Stores sales data for products."
        verbose_name = _("Sales Data")
        verbose_name_plural = _("Sales Data")
        unique_together = ["product", "date", "currency"]

    def __str__(self):
        return f"{self.product.name} - {self.date}"
