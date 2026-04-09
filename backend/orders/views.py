from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    OrderSerializer,
    FeedbackSerializer,
    ContactSerializer
)
from .models import Order


# ==================================
# EMAIL HELPERS
# ==================================
def send_order_emails(order):
    try:
        admin_email = EmailMessage(
            subject="New Service Order - KDK",
            body=f"""
New order received

Name: {order.name}
Email: {order.email}
Phone: {order.phone}
Service: {order.service}
Message: {order.message}
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.DEFAULT_FROM_EMAIL],
        )

        if getattr(order, "file", None):
            try:
                if order.file and order.file.name:
                    admin_email.attach_file(order.file.path)
            except Exception as e:
                print("FILE ATTACH ERROR:", e)

        admin_email.send(fail_silently=True)

    except Exception as e:
        print("ADMIN MAIL ERROR:", e)

    try:
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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.email],
            fail_silently=True,
        )
    except Exception as e:
        print("CUSTOMER MAIL ERROR:", e)


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
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        print("CONTACT MAIL ERROR:", e)


# ==================================
# ORDER API
# ==================================
@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def create_order(request):
    try:
        serializer = OrderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES.get("file")

        order = Order.objects.create(
            name=serializer.validated_data["name"],
            email=serializer.validated_data["email"],
            phone=serializer.validated_data["phone"],
            service=serializer.validated_data["service"],
            message=serializer.validated_data.get("message", ""),
            file=file_obj if file_obj else None
        )
        
        return Response(
            {
                "success": True,
                "message": "Order placed successfully"
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("ORDER ERROR:", str(e))
        return Response(
            {
                "success": False,
                "message": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ==================================
# FEEDBACK API
# ==================================
@api_view(["POST"])
@parser_classes([JSONParser, FormParser])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "message": "Feedback submitted successfully"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


# ==================================
# CONTACT API
# ==================================
@api_view(["POST"])
@parser_classes([JSONParser, FormParser])
def send_contact_message(request):
    serializer = ContactSerializer(data=request.data)

    if serializer.is_valid():
        contact = serializer.save()
        send_contact_email(contact)

        return Response(
            {
                "success": True,
                "message": "Saved successfully"
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "success": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )