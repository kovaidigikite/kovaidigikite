from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model("auth", "User")

    if not User.objects.filter(username="kdkadmin").exists():
        User.objects.create_superuser(
            username="kdkadmin",
            email="kovaidigikites@gmail.com",
            password="Kdk@12345"
        )


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]