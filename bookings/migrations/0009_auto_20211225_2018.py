# Generated by Django 3.2.4 on 2021-12-25 10:48

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_booking_qr_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_date',
            field=models.DateField(default=datetime.datetime(2021, 12, 25, 10, 48, 18, 945669, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 25, 10, 48, 18, 945669, tzinfo=utc)),
        ),
    ]
