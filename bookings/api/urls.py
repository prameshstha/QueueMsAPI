from .views import GetAvailableTimeSlot, AllBookingsListCreate, GetBookingDetails, GetBookingDetailsByUser, CheckIn, CheckedInQueue

from django.urls import path

urlpatterns = [
    path('available-time/', GetAvailableTimeSlot.as_view(), name='available-time'),  # post request only -
    #  get and post request only -
    path('list-create-booking/', AllBookingsListCreate.as_view(), name='list-create-booking'),
    #   get, patch and delete request only -
    path('booking-details/<int:pk>/', GetBookingDetails.as_view(), name='booking-details'),
    #   get, patch and delete request only -
    path('user-booking-details/<int:patient_id>/', GetBookingDetailsByUser.as_view(), name='user-booking-details'),
    path('check-in/<int:patient_id>/', CheckIn.as_view(), name='check-in'),
    path('checked-in-queue/<int:patient_id>/', CheckedInQueue.as_view(), name='check-in-list'),
]
