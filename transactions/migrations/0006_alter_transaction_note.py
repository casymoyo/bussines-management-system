# Generated by Django 4.2.6 on 2023-10-27 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("transactions", "0005_alter_transaction_owing_alter_transaction_resource"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="note",
            field=models.TextField(blank=True),
        ),
    ]