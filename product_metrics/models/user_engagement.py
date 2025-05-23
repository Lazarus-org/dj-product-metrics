from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from product_metrics.models.product import Product


class UserEngagement(models.Model):
    """
    A model representing user engagement metrics for products.

    This model tracks user engagement metrics including active users and
    churn rate, providing insights into product usage and user retention.

    Attributes:
        product (Product): The associated product
        date (date): The date of the engagement data
        active_users (int): Number of active users
        churn_rate (float): Percentage of users who stopped using the product
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="user_engagement",
        verbose_name=_("Product"),
        help_text=_("The product associated with this user engagement data."),
        db_comment="Foreign key to the Product model.",
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("The date of the user engagement data."),
        db_comment="Stores the date of the user engagement data.",
        db_index=True
    )
    active_users = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_("Active Users"),
        help_text=_("The number of active users on this date."),
        db_comment="Stores the number of active users.",
    )
    churn_rate = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name=_("Churn Rate"),
        help_text=_("The churn rate (in percentage) on this date."),
        db_comment="Stores the churn rate in percentage.",
    )

    class Meta:
        db_table_comment = "Stores user engagement data for products."
        verbose_name = _("User Engagement")
        verbose_name_plural = _("User Engagement")
        unique_together = ["product", "date"]

    def __str__(self):
        return f"{self.product.name} - {self.date}"
