# Generated by Django 4.2.7 on 2024-05-25 15:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("tipoint_ticroix", "0002_verifuser"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="verifuser",
            name="pseudo",
        ),
    ]