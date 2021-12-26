from django.contrib import admin
from .models import Booking, BusinessHours, TimeSlots, BookingStatus, AvailableDoctor


# Register your models here.
# class DocTimeSolt(admin.TabularInline):
#     model = TimeSlots
#
#
# class TimeSlotDoc(admin.ModelAdmin):
#     inlines = [DocTimeSolt]


admin.site.register(Booking)
admin.site.register(BusinessHours)
admin.site.register(TimeSlots, )
admin.site.register(BookingStatus)
admin.site.register(AvailableDoctor)
