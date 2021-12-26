from django.db.models import Q
from rest_framework import serializers

from accounts.models import CustomUser
from bookings.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(write_only=True)
    class Meta:
        model = Booking
        fields = ['doc_id', 'booking_date']
        # fields = '__all__'


class AllBookingSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(write_only=True)
    class Meta:
        model = Booking
        fields = '__all__'

    def save(self):
        patient_id = self.validated_data['patient_id']
        existing_booking = Booking.objects.filter(
            Q(booking_status='Booked') | Q(booking_status='CheckedIn') | Q(booking_status='OnCall'),
            patient_id=patient_id)
        print('existing booking', existing_booking)
        if existing_booking:
            raise serializers.ValidationError({'error': 'Booking already exists or CheckedIn or OnCall'}, 401)
        # book = Booking(booking_date=self.validated_data['booking_date'])
        # book.save()

        try:
            booking = Booking.objects.create(**self.validated_data)
        except TypeError as error:
            raise serializers.ValidationError(error)
        return booking


class CheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class queue_num_field(serializers.IntegerField):
    def to_representation(self, patient):
        print('valueeee', patient)
        checked_in_list = Booking.objects.filter(booking_status='CheckedIn').order_by('-updated_at')
        try:
            # patient = Booking.objects.get(patient_id=9, booking_status='CheckedIn')
            print(patient)
            print(checked_in_list)
            print(list(checked_in_list).index(patient))
            queue_num = list(checked_in_list).index(patient)

            return queue_num+1
        except:
            return 111


class CheckedInQueueNum(serializers.ModelSerializer):
    queue_num = queue_num_field(source='*')

    class Meta:
        model = Booking
        fields = ['doc_id', 'booking_date', 'queue_num']
        # fields = '__all__'
