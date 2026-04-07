from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from orders.models import Order
from .serializers import OrderSerializer, FeedbackSerializer, ContactSerializer
from .tasks import send_order_emails_task, send_contact_email_task


# ==================================
# ORDER EMAIL HELPER
# ==================================
def send_order_emails(order):
    # ✅ Admin mail
    try:
        email = EmailMessage(
            subject="New Service Order - KDK",
            body=f"""
New order received

Name: {order.name}
Email: {order.email}
Phone: {order.phone}
Service: {order.service}
Message: {order.message}
            """,
            from_email=settings.EMAIL_HOST_USER,
            to=[settings.EMAIL_HOST_USER]
        )

        # ✅ Safe file attach
        if order.file and hasattr(order.file, "path"):
            try:
                email.attach_file(order.file.path)
            except Exception as file_error:
                print("FILE ATTACH ERROR:", str(file_error))

        email.send(fail_silently=False)
        print("ADMIN ORDER MAIL SENT")

    except Exception as e:
        print("ADMIN ORDER MAIL ERROR:", str(e))

    # ✅ Customer confirmation mail
    try:
        if order.email:
            send_mail(
                subject="Order Received - Kovai Digi Kites",
                message=f"""
Hi {order.name},

Thank you for choosing Kovai Digi Kites.

Your order for "{order.service}" has been received successfully.

Our team will contact you soon.

Regards,
KDK Team
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.email],
                fail_silently=False
            )
            print("CUSTOMER ORDER MAIL SENT")

    except Exception as e:
        print("CUSTOMER MAIL ERROR:", str(e))


# ==================================
# CONTACT EMAIL HELPER
# ==================================
def send_contact_email(contact):
    try:
        send_mail(
            subject="New Contact Message - KDK",
            message=f"""
Name: {contact.name}
Email: {contact.email}
Phone: {contact.phone}

Message:
{contact.message}
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False
        )
        print("CONTACT MAIL SENT")

    except Exception as e:
        print("CONTACT MAIL ERROR:", str(e))


# ==================================
# ORDER API
# ==================================
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    if not serializer.is_valid():
        print("ORDER ERRORS:", serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    order = serializer.save()
# ✅ Background email task (Celery)
try:
    send_order_emails_task.delay({
        "name": Order.name,
        "email": Order.email,
        "phone": Order.phone,
        "service": Order.service,
        "message": Order.message
    })
except Exception as e:
    print("CELERY ORDER TASK ERROR:", str(e))


# ==================================
# FEEDBACK API
# ==================================
@api_view(["POST"])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "success": True,
            "message": "Feedback submitted successfully"
        })

    print("FEEDBACK ERRORS:", serializer.errors)
    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


# ==================================
# CONTACT API
# ==================================
@api_view(["POST"])
def send_contact_message(request):
    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():
        print("CONTACT ERRORS:", serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    contact = serializer.save()

      # ✅ Background contact email task
    try:
        send_contact_email_task.delay({
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "message": contact.message
        })
    except Exception as e:
        print("CELERY CONTACT TASK ERROR:", str(e))
    return Response({
        "success": True,
        "message": "Saved successfully"
    })