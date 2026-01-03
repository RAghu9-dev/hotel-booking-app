
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('my-bookings/', views.my_bookings_view, name='my-bookings'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking_view, name='cancel-booking'),
    path('<slug>/hotel-details', views.hotel_details_view, name="hotel-details")
]
