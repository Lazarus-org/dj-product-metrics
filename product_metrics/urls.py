from django.urls import path

from product_metrics.views import ProductMetricsListView, ProductMetricsDetailView

app_name = "product_metrics"

urlpatterns = [
    path("", ProductMetricsListView.as_view(), name="product_metrics_list"),
    path("<int:product_id>/", ProductMetricsDetailView.as_view(), name="product_metrics_detail"),
]
