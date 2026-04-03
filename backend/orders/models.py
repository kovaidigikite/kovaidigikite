import uuid
from django.db import models

class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    service = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='orders/', null=True, blank=True)
    status = models.CharField(max_length=50, default='Order Placed')
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    order_details = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    design_feedback = models.IntegerField()
    customer_feedback = models.IntegerField()
    overall_rating = models.IntegerField()
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)