from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({
        "message": "Kovai Digi Kite Backend Live ✅"
    })


def health(request):
    return JsonResponse({
        "status": "ok"
    })


urlpatterns = [
    path("", home),              # homepage
    path("health/", health),     # health check
    path("api/", include("orders.urls")),
    path("admin/", admin.site.urls),
]