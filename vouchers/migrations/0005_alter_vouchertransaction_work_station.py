# Generated by Django 4.2.6 on 2023-11-01 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0013_alter_client_count"),
        ("vouchers", "0004_vouchertransaction_work_station"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vouchertransaction",
            name="work_station",
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to="client.workstation"),
        ),
    ]