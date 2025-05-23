from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from product_metrics.models.product import Product


class CustomerFeedback(models.Model):
    """
    A model representing customer feedback for products.

    This model stores customer ratings and feedback for products,
    helping in understanding customer satisfaction and areas for
    improvement.

    Attributes:
        product (Product): The associated product
        date (date): The date of the feedback
        rating (float): Customer rating out of 5
        feedback (str): Additional feedback provided by the customer
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="customer_feedback",
        verbose_name=_("Product"),
        help_text=_("The product associated with this customer feedback."),
        db_comment="Foreign key to the Product model.",
    )
    date = models.DateField(
        verbose_name=_("Date"),
        help_text=_("The date of the customer feedback."),
        db_comment="Stores the date of the customer feedback.",
        db_index=True
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Rating"),
        help_text=_("The rating given by the customer (out of 5)."),
        db_comment="Stores the customer rating out of 5.",
    )
    feedback = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Feedback"),
        help_text=_("Additional feedback provided by the customer."),
        db_comment="Stores additional customer feedback.",
    )

    class Meta:
        db_table_comment = "Stores customer feedback for products."
        verbose_name = _("Customer Feedback")
        verbose_name_plural = _("Customer Feedback")
        unique_together = ["product", "date"]

    def __str__(self):
        return f"{self.product.name} - {self.date}"
