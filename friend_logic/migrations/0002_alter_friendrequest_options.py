# Generated by Django 5.0.6 on 2024-07-22 07:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("friend_logic", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="friendrequest",
            options={"ordering": ["timestamp"]},
        ),
    ]