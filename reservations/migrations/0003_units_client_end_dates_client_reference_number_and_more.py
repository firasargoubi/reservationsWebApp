# Generated by Django 5.0.7 on 2024-08-02 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_remove_reservation_code_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Units',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short', models.TextField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='end_dates',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='reference_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='start_date',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='unit',
            field=models.IntegerField(null=True),
        ),
    ]
