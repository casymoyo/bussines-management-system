# Generated by Django 4.2.6 on 2023-10-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0002_alter_expensecancellation_reason"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="description",
            field=models.CharField(blank=True, default="", max_length=255),
            preserve_default=False,
        ),
    ]
