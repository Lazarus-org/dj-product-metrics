from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _

class Product(models.Model):
    name = models.CharField(
        max_length=100,
        help_text=_("The name of the product."),
        db_comment="Stores the name of the product."
    )
    description = models.TextField(
        blank=True, null=True,
        help_text=_("A brief description of the product."),
        db_comment="Stores a description of the product."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time when the product was created."),
        db_comment="Stores the creation timestamp of the product."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The date and time when the product was last updated."),
        db_comment="Stores the last update timestamp of the product."
    )

    class Meta:
        db_table_comment = "Stores information about products."

    def __str__(self):
        return self.name

class SalesData(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sales_data',
        help_text=_("The product associated with this sales data."),
        db_comment="Foreign key to the Product model."
    )
    date = models.DateField(
        help_text=_("The date of the sales data."),
        db_comment="Stores the date of the sales data."
    )
    units_sold = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text=_("The number of units sold on this date."),
        db_comment="Stores the number of units sold."
    )
    revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("The revenue generated on this date."),
        db_comment="Stores the revenue generated."
    )

    class Meta:
        db_table_comment = "Stores sales data for products."

    def __str__(self):
        return f"{self.product.name} - {self.date}"

class UserEngagement(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='user_engagement',
        help_text=_("The product associated with this user engagement data."),
        db_comment="Foreign key to the Product model."
    )
    date = models.DateField(
        help_text=_("The date of the user engagement data."),
        db_comment="Stores the date of the user engagement data."
    )
    active_users = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        help_text=_("The number of active users on this date."),
        db_comment="Stores the number of active users."
    )
    churn_rate = models.FloatField(
        validators=[MinValueValidator(0)],
        help_text=_("The churn rate (in percentage) on this date."),
        db_comment="Stores the churn rate in percentage."
    )

    class Meta:
        db_table_comment = "Stores user engagement data for products."

    def __str__(self):
        return f"{self.product.name} - {self.date}"

class CustomerFeedback(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='customer_feedback',
        help_text=_("The product associated with this customer feedback."),
        db_comment="Foreign key to the Product model."
    )
    date = models.DateField(
        help_text=_("The date of the customer feedback."),
        db_comment="Stores the date of the customer feedback."
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text=_("The rating given by the customer (out of 5)."),
        db_comment="Stores the customer rating out of 5."
    )
    feedback = models.TextField(
        blank=True, null=True,
        help_text=_("Additional feedback provided by the customer."),
        db_comment="Stores additional customer feedback."
    )

    class Meta:
        db_table_comment = "Stores customer feedback for products."

    def __str__(self):
        return f"{self.product.name} - {self.date}"