# Generated by Django 4.2.6 on 2023-10-22 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0009_alter_client_station_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="station_number",
            field=models.OneToOneField(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="client.workstation"
            ),
        ),
    ]