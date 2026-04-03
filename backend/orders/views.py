from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import OrderSerializer, FeedbackSerializer, ContactSerializer


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def create_order(request):
    serializer = OrderSerializer(data=request.data)

    # ✅ debug serializer errors
    if not serializer.is_valid():
        print("ORDER ERRORS:", serializer.errors)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    order = serializer.save()

    # ✅ company mail with attachment
    try:
        email = EmailMessage(
            subject='New Service Order - KDK',
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

        # ✅ attach uploaded file/image
        if order.file:
            email.attach_file(order.file.path)

        email.send(fail_silently=False)

    except Exception as e:
        print("ADMIN ORDER MAIL ERROR:", e)

    # ✅ customer confirmation mail
    try:
        send_mail(
            subject='Order Received - Kovai Digi Kites',
            message=f"""
Hi {order.name},

Thank you for choosing Kovai Digi Kites

Your order for "{order.service}" has been received successfully.

Our team will contact you soon.

Regards,
KDK Team
            """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[order.email],
            fail_silently=False
        )
    except Exception as e:
        print("CUSTOMER MAIL ERROR:", e)

    return Response({
        "success": True,
        "message": "Order placed successfully"
    })


@api_view(['POST'])
def submit_feedback(request):
    serializer = FeedbackSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"success": True})

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)


@api_view(['POST'])
def send_contact_message(request):
    serializer = ContactSerializer(data=request.data)

    if not serializer.is_valid():
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=400)

    contact = serializer.save()

    try:
        send_mail(
            subject='New Contact Message - KDK',
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
    except Exception as e:
        print("MAIL ERROR:", e)

    return Response({
        "success": True,
        "message": "Saved successfully"
    })