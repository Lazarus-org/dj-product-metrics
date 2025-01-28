from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, SalesData, UserEngagement, CustomerFeedback

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'units_sold', 'revenue')
    search_fields = ('product__name', 'date')
    list_filter = ('product', 'date')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('product', 'date', 'units_sold', 'revenue')
        }),
    )

@admin.register(UserEngagement)
class UserEngagementAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'active_users', 'churn_rate')
    search_fields = ('product__name', 'date')
    list_filter = ('product', 'date')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('product', 'date', 'active_users', 'churn_rate')
        }),
    )

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('product', 'date', 'rating', 'feedback')
    search_fields = ('product__name', 'date', 'feedback')
    list_filter = ('product', 'date', 'rating')
    date_hierarchy = 'date'
    fieldsets = (
        (None, {
            'fields': ('product', 'date', 'rating', 'feedback')
        }),
    )