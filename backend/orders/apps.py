from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()

        if not User.objects.filter(username='kdkadmin').exists():
            User.objects.create_superuser(
                username='kdkadmin',
                email='kovaidigikites@gmail.com',
                password='Kdk@12345'
            )