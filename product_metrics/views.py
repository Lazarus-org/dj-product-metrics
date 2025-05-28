from django.core.exceptions import PermissionDenied
from django.db.models import Count, Avg
from django.views.generic import ListView, DetailView
from product_metrics.models import Product, SalesData, UserEngagement, CustomerFeedback
from product_metrics.settings.conf import config


class BaseView:
    """Base view class for views that handles common authentication logic."""

    permission_classes = [config.view_permission_class]

    def get_permissions(self):
        """Instantiate and return the list of permissions that this view requires."""
        return [permission() for permission in self.permission_classes if permission]

    def check_permissions(self, request):
        """Check if the request should be permitted, raising PermissionDenied if not."""
        for permission in self.get_permissions():
            if not hasattr(
                permission, "has_permission"
            ) or not permission.has_permission(request, self):
                raise PermissionDenied()

    def dispatch(self, request, *args, **kwargs):
        """Handle request dispatch with permission checks."""
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)


class ProductMetricsListView(BaseView, ListView):
    """View for displaying a list of products with their key metrics."""

    template_name = "product_metrics_list.html"
    model = Product
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        """Get the context data for the template."""
        context = super().get_context_data(**kwargs)
        context["products"] = []

        for product in self.get_queryset():
            # Get latest sales data
            latest_sales = (
                SalesData.objects.filter(product=product).order_by("-date").first()
            )

            # Get latest engagement data
            latest_engagement = (
                UserEngagement.objects.filter(product=product).order_by("-date").first()
            )

            # Get aggregated feedback data
            feedback_stats = CustomerFeedback.objects.filter(product=product).aggregate(
                avg_rating=Avg("rating"), total_feedback=Count("id")
            )

            product_data = {
                "product": product,
                "latest_revenue": latest_sales.revenue if latest_sales else 0,
                "latest_units_sold": latest_sales.units_sold if latest_sales else 0,
                "active_users": (
                    latest_engagement.active_users if latest_engagement else 0
                ),
                "churn_rate": (
                    round(latest_engagement.churn_rate, 2) if latest_engagement else 0
                ),
                "average_rating": feedback_stats["avg_rating"] or 0,
                "total_feedback": feedback_stats["total_feedback"] or 0,
            }
            context["products"].append(product_data)

        return context


class ProductMetricsDetailView(BaseView, DetailView):
    """View for displaying detailed metrics for a specific product."""

    template_name = "product_metrics_detail.html"
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get_context_data(self, **kwargs):
        """Get the context data for the template."""
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Fetch sales data
        sales_data = SalesData.objects.filter(product=product).order_by("date")
        sales_labels = [data.date.strftime("%Y-%m-%d") for data in sales_data]
        sales_revenue = [float(data.revenue) for data in sales_data]
        sales_units_sold = [data.units_sold for data in sales_data]

        # Fetch user engagement data
        engagement_data = UserEngagement.objects.filter(product=product).order_by(
            "date"
        )
        engagement_labels = [data.date.strftime("%Y-%m-%d") for data in engagement_data]
        active_users = [data.active_users for data in engagement_data]
        churn_rate = [round(data.churn_rate, 2) for data in engagement_data]

        # Fetch aggregated customer feedback data
        feedback_aggregated = (
            CustomerFeedback.objects.filter(product=product)
            .values("date")
            .annotate(feedback_count=Count("id"), average_rating=Avg("rating"))
            .order_by("date")
        )
        feedback_labels = [
            entry["date"].strftime("%Y-%m-%d") for entry in feedback_aggregated
        ]
        feedback_counts = [entry["feedback_count"] for entry in feedback_aggregated]
        average_ratings = [entry["average_rating"] for entry in feedback_aggregated]

        context.update(
            {
                "sales_labels": sales_labels,
                "sales_revenue": sales_revenue,
                "sales_units_sold": sales_units_sold,
                "engagement_labels": engagement_labels,
                "active_users": active_users,
                "churn_rate": churn_rate,
                "feedback_labels": feedback_labels,
                "feedback_counts": feedback_counts,
                "average_ratings": average_ratings,
            }
        )

        return context
