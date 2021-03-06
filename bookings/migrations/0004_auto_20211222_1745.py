# Generated by Django 3.2.4 on 2021-12-22 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_remove_timeslots_doc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booking_status',
            field=models.CharField(choices=[('Booked', 'Booked'), ('CheckedIn', 'CheckedIn'), ('OnCall', 'OnCall'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], max_length=255),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_time',
            field=models.CharField(choices=[('--Select Time--', '--Select Time--'), ('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30')], max_length=255),
        ),
    ]
