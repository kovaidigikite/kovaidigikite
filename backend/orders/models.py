
from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(default="unknown@example.com")
    phone = models.CharField(max_length=20, default="0000000000")
    service = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(
    upload_to="orders/%Y/%m/%d/",
    blank=True,
    null=True
)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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