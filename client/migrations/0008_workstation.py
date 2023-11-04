# Generated by Django 4.2.6 on 2023-10-20 12:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0007_alter_account_client"),
    ]

    operations = [
        migrations.CreateModel(
            name="WorkStation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("station", models.CharField(max_length=4)),
                (
                    "status",
                    models.CharField(choices=[("occupied", "occupied"), ("vaccant", "vaccant")], max_length=50),
                ),
            ],
        ),
    ]
