from django.db.models import Count, Avg
from django.shortcuts import render, get_object_or_404
from .models import Product, SalesData, UserEngagement, CustomerFeedback

def product_metrics(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Fetch sales data
    sales_data = SalesData.objects.filter(product=product).order_by('date')
    sales_labels = [data.date.strftime('%Y-%m-%d') for data in sales_data]
    sales_revenue = [float(data.revenue) for data in sales_data]
    sales_units_sold = [data.units_sold for data in sales_data]

    # Fetch user engagement data
    engagement_data = UserEngagement.objects.filter(product=product).order_by('date')
    engagement_labels = [data.date.strftime('%Y-%m-%d') for data in engagement_data]
    active_users = [data.active_users for data in engagement_data]
    churn_rate = [data.churn_rate for data in engagement_data]

    # Fetch aggregated customer feedback data
    feedback_aggregated = (
        CustomerFeedback.objects.filter(product=product)
        .values('date')
        .annotate(
            feedback_count=Count('id'),
            average_rating=Avg('rating')
        )
        .order_by('date')
    )
    feedback_labels = [entry['date'].strftime('%Y-%m-%d') for entry in feedback_aggregated]
    feedback_counts = [entry['feedback_count'] for entry in feedback_aggregated]
    average_ratings = [entry['average_rating'] for entry in feedback_aggregated]

    context = {
        'product': product,
        'sales_labels': sales_labels,
        'sales_revenue': sales_revenue,
        'sales_units_sold': sales_units_sold,
        'engagement_labels': engagement_labels,
        'active_users': active_users,
        'churn_rate': churn_rate,
        'feedback_labels': feedback_labels,
        'feedback_counts': feedback_counts,
        'average_ratings': average_ratings,
    }

    return render(request, 'product_metrics.html', context)
