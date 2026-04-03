from django.contrib import admin
from .models import Order, Feedback, ContactMessage


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'phone',
        'service',
        'created_at'
    )
    search_fields = ('name', 'email', 'phone', 'service')
    list_filter = ('service', 'created_at')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'overall_rating', 'created_at')


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')