from datetime import datetime
from django.contrib.auth import logout, authenticate
from django.contrib.auth.hashers import check_password, make_password
from django.core import serializers
from django.core.serializers import serialize
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.utils import timezone
from pytz.reference import Local
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookingSerializer, AllBookingSerializer, CheckInSerializer, CheckedInQueueNum
from accounts.models import CustomUser
from bookings.models import Booking, TimeSlots, BusinessHours

import random
import qrcode
from PIL import Image, ImageDraw
from django.core.files import File
from io import BytesIO
import random
import string


class GetAvailableTimeSlot(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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
        # print(request.data)
        serializer = BookingSerializer(data=request.data)
        # print(serializer.is_valid())
        # print(serializer.errors)

        if serializer.is_valid():
            print(request.data)
            # date = '2021-12-21'
            # serializers = TimeSlotsSerializer(data=request.data)
            date = request.data['booking_date']
            doc_id = request.data['doc_id']

            tSlot = []
            timeslotList = []
            if date:
                bookings = Booking.objects.filter(booking_date=date, doc_id=doc_id)
                print(bookings)
                doc = CustomUser.objects.filter(is_doc=True)
                timeslot = TimeSlots.objects.all()
                for t in timeslot:
                    timeslotList.append(t.time_slot)
                print(timeslotList)
                for b in bookings:
                    tSlot.append(b.booking_time)
                #     get datetime.now
                datetime_now = datetime.now(tz=Local)
                date_now = datetime.now(tz=Local).date()
                print(date, 'date now', date_now, date == str(date_now))
                hour_min_now = str(datetime_now.hour) + ':' + str(datetime_now.minute)  # for hour
                if date == str(date_now):
                    future_time = list(filter(lambda x: x > hour_min_now, timeslotList))
                    print(future_time)
                    print('datetime now', datetime_now, 'a', hour_min_now)
                    available_timeSlot = list(filter(lambda x: x not in tSlot, future_time))
                    available_timeSlot.insert(0, '--Select Time--')
                else:
                    print('datetime now', datetime_now, 'a', hour_min_now)
                    available_timeSlot = list(filter(lambda x: x not in tSlot, timeslotList))

                print(tSlot)
                print(available_timeSlot)
                # print(available_timeSlot)
                # json_timeslot = json.dumps(available_timeSlot, default=lambda x: x.__dict__)

                return Response(available_timeSlot, 200)
        return Response(serializer.errors)


class AllBookingsListCreate(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    def get_queryset(self):
        list = Booking.objects.filter(booking_status='Booked')
        return list

    # queryset = Booking.objects.all()
    serializer_class = AllBookingSerializer


class CheckedInQueue(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        print(patient_id)
        # checked_in_list = Booking.objects.filter(booking_status='CheckedIn').order_by('-updated_at')
        patient = Booking.objects.filter(patient_id=patient_id, booking_status='CheckedIn')
        print(patient)
        # print(checked_in_list)
        return patient

    # queryset = Booking.objects.all()
    serializer_class = CheckedInQueueNum


class GetBookingDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()
    serializer_class = AllBookingSerializer


class GetBookingDetailsByUser(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        print(patient_id)
        # get the latest booking of the patients
        qs = Booking.objects.filter(patient_id=patient_id).order_by('-id')[:1]
        return qs

    # queryset = Booking.objects.all()
    serializer_class = AllBookingSerializer
    lookup_field = 'patient_id'


class CheckIn(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     patient_id = self.kwargs['pk']
    #     print(patient_id)
    #     book = Booking.objects.filter(patient_id=patient_id, booking_status='Booked')
    #     print(book)
    #     return book
    queryset = Booking.objects.all()
    serializer_class = CheckInSerializer
    lookup_field = 'patient_id'

    def GetQrCode(self):
        qr_code_name = f'{random.choice(string.ascii_letters) + str(random.randint(0, 99999)) + random.choice(string.ascii_letters)}'
        return qr_code_name

    def update(self, request, *args, **kwargs):
        patient_id = self.kwargs['patient_id']
        # patient_id = validated_data['patient_id']
        print(patient_id, 'patient id')
        try:
            existing_booking = Booking.objects.get(booking_status='Booked', patient_id=patient_id)
        except:
            return Response({'error': 'Booking not found for this patient'}, 401)
        if existing_booking:
            print(existing_booking)
            existing_booking.qr_code = self.GetQrCode()
            qr_image_content = qrcode.make(existing_booking.qr_code)  # add the content in the qrcode
            qr_offset = Image.new('RGB', (310, 310), 'white')
            qr_offset.paste(qr_image_content)
            files_name = f'{existing_booking.qr_code}qr.png'
            print(files_name)
            stream = BytesIO()
            qr_offset.save(stream, 'PNG')
            existing_booking.qr_code_image.save(files_name, File(stream))
            existing_booking.booking_status = 'CheckedIn'

            qr_offset.close()
            saved = existing_booking.save()
            dict = model_to_dict(existing_booking)
            print(dict)
            json_booking = json.dumps(dict, default=str)

            return Response(json_booking, content_type='application/json')
            # serializers.data = existing_booking
            # super().save(*args, **kwargs)
        else:
            return Response({'error': 'Booking not found for this patient'}, 401)
