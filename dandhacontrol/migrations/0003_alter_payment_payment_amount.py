# Generated by Django 4.1.4 on 2023-04-28 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dandhacontrol', '0002_rename_recharge_date_device_expiry_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
