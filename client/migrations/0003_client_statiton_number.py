# Generated by Django 4.2.6 on 2023-10-15 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("client", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="statiton_number",
            field=models.CharField(default="A", max_length=50),
            preserve_default=False,
        ),
    ]
