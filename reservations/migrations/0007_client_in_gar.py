# Generated by Django 5.0.7 on 2024-08-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_remove_garage_client_client_garage_garage_occupied'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='in_gar',
            field=models.BooleanField(null=True),
        ),
    ]
