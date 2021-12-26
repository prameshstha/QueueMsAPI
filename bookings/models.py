from calendar import calendar
from datetime import datetime
from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField
# Create your models here.
from pytz.reference import Local

from accounts.models import CustomUser


TIMESLOT_LIST = (
    ('--Select Time--', '--Select Time--'),
    ('09:00', '09:00'),
    ('09:30', '09:30'),
    ('10:00', '10:00'),
    ('10:30', '10:30'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('12:30', '12:30'),
    ('13:00', '13:00'),
    ('13:30', '13:30'),
    ('14:00', '14:00'),
    ('14:30', '14:30'),
    ('15:00', '15:00'),
    ('15:30', '15:30'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
)
DAY_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday')
)


class AvailableDoctor(models.Model):
    doc = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    available_day = MultiSelectField(choices=DAY_CHOICES, null=True, blank=True)
    # available_time = MultiSelectField(choices=TIMESLOT_LIST, null=True, blank=True)
    # time_slot = MultiSelectField(TIMESLOT_LIST)
    # available_time_from = models.TimeField(default=datetime.now())
    # available_time_to = models.TimeField(default=datetime.now())


class TimeSlots(models.Model):
    time_slot = models.CharField(max_length=255, choices=TIMESLOT_LIST)

    # doc = models.ForeignKey(AvailableDoctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.time_slot


class BusinessHours(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    )
    # DAY_CHOICES = tuple(enumerate(calendar.day_name))
    open_at = models.TimeField(null=True, blank=True)
    close_at = models.TimeField(null=True, blank=True)
    off_days = MultiSelectField(choices=DAY_CHOICES, null=True, blank=True)

    def __str__(self):
        return 'Business Hour'


class BookingStatus(models.Model):
    BOOKING_STATUS_LIST = (
        ('Booked', 'Booked'),
        ('CheckedIn', 'CheckedIn'),
        ('OnCall', 'OnCall'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),)
    booking_status = models.CharField(max_length=255, choices=BOOKING_STATUS_LIST)

    def __str__(self):
        return self.booking_status


class Booking(models.Model):
    BOOKING_STATUS_LIST = (
        ('Booked', 'Booked'),
        ('CheckedIn', 'CheckedIn'),
        ('OnCall', 'OnCall'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),)
    TIMESLOT_LIST = (
        ('--Select Time--', '--Select Time--'),
        ('09:00', '09:00'),
        ('09:30', '09:30'),
        ('10:00', '10:00'),
        ('10:30', '10:30'),
        ('11:00', '11:00'),
        ('11:30', '11:30'),
        ('12:00', '12:00'),
        ('12:30', '12:30'),
        ('13:00', '13:00'),
        ('13:30', '13:30'),
        ('14:00', '14:00'),
        ('14:30', '14:30'),
        ('15:00', '15:00'),
        ('15:30', '15:30'),
        ('16:00', '16:00'),
        ('16:30', '16:30'),
    )

    # def UniqueToken(self):
    #     # import EAN13 from barcode module
    #     from barcode import EAN13
    #
    #     # Make sure to pass the number as string
    #     number = '5901234123457'
    #
    #     # Now, let's create an object of EAN13
    #     # class and pass the number
    #     my_code = EAN13(number)
    #
    #     # Our barcode is ready. Let's save it.
    #     # my_code.save("new_code")
    #     # datetime = datetime.now()
    #     utoken = ''
    #     print(my_code)
    #     return my_code

    booking_status = models.CharField(max_length=255, choices=BOOKING_STATUS_LIST)
    booking_time = models.CharField(max_length=255, choices=TIMESLOT_LIST)
    patient_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_id')
    doc_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doc_id')
    booking_date = models.DateField(default=datetime.now(tz=Local))
    created_at = models.DateTimeField(default=datetime.now(tz=Local))
    updated_at = models.DateTimeField(auto_now=True)
    qr_code = models.CharField(max_length=255, blank=True)
    qr_code_image = models.ImageField(blank=True, upload_to='booking_qrcode')

    def __str__(self):
        return str(self.booking_time) + str(self.booking_status)

    # def save(self, *args, **kwargs):
    #     self.qr_code = self.GetQrCode()
    #     qr_image_content = qrcode.make(self.qr_code)  # add the content in the qrcode
    #     qr_offset = Image.new('RGB', (310, 310), 'white')
    #     qr_offset.paste(qr_image_content)
    #     files_name = f'{self.qr_code}qr.png'
    #     stream = BytesIO()
    #     qr_offset.save(stream, 'PNG')
    #     self.qr_code_image.save(files_name, File(stream), save=False)
    #     qr_offset.close()
    #     super().save(*args, **kwargs)
