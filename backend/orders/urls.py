from django.urls import path
from .views import create_order, submit_feedback, send_contact_message

urlpatterns = [
    path('order/', create_order),
    path('feedback/', submit_feedback),
    path('contact/', send_contact_message),
]