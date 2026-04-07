import os
import requests
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .serializers import (
    OrderSerializer,
    FeedbackSerializer,
    ContactSerializer
)


# ==================================
# BREVO EMAIL HELPER
# ==================================
def send_brevo_email(subject, html_content, to_email):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Kovai Digi Kite",
            "email": "kovaidigikite@gmail.com"
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content
    }

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        timeout=20
    )

    print("BREVO STATUS:", response.status_code, response.text)


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

    # ✅ admin mail
    try:
        send_brevo_email(
            "New Service Order - KDK",
            f"""
            <h2>New Order Received</h2>
            <p><b>Name:</b> {order.name}</p>
            <p><b>Email:</b> {order.email}</p>
            <p><b>Phone:</b> {order.phone}</p>
            <p><b>Service:</b> {order.service}</p>
            <p><b>Message:</b> {order.message}</p>
            """,
            "kovaidigikites@gmail.com"
        )
    except Exception as e:
        print("BREVO ADMIN ORDER MAIL ERROR:", str(e))

    # ✅ customer confirmation
    try:
        if order.email:
            send_brevo_email(
                "Order Received - Kovai Digi Kite",
                f"""
                <h2>Hi {order.name},</h2>
                <p>Thank you for choosing Kovai Digi Kite.</p>
                <p>Your order for <b>{order.service}</b> has been received successfully.</p>
                <p>Our team will contact you soon.</p>
                <br>
                <p>Regards,<br>KDK Team</p>
                """,
                order.email
            )
    except Exception as e:
        print("BREVO CUSTOMER ORDER MAIL ERROR:", str(e))

    return Response({
        "success": True,
        "message": "Order placed successfully"
    })


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

    try:
        send_brevo_email(
            "New Contact Message - KDK",
            f"""
            <h2>New Contact Message</h2>
            <p><b>Name:</b> {contact.name}</p>
            <p><b>Email:</b> {contact.email}</p>
            <p><b>Phone:</b> {contact.phone}</p>
            <p><b>Message:</b> {contact.message}</p>
            """,
            "kovaidigikites@gmail.com"
        )
    except Exception as e:
        print("BREVO CONTACT MAIL ERROR:", str(e))

    return Response({
        "success": True,
        "message": "Saved successfully"
    })