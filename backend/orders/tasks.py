from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail, EmailMessage


@shared_task
def send_order_emails_task(order_data):
    email = EmailMessage(
        subject="New Service Order - KDK",
        body=f"""
New order received

Name: {order_data['name']}
Email: {order_data['email']}
Phone: {order_data['phone']}
Service: {order_data['service']}
Message: {order_data['message']}
        """,
        from_email=settings.EMAIL_HOST_USER,
        to=[settings.EMAIL_HOST_USER]
    )
    email.send(fail_silently=False)