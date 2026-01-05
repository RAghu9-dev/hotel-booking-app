from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
import random
from datetime import date, datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Prefetch

def setImages(hotels):
    for hotel in hotels:
        # Get the first image for this hotel
        first_image = hotel.hotel_images.first()
        if first_image:
            hotel.image_url = first_image.image.url
        else:
            hotel.image_url = None
    return hotels

@login_required
def index(request):
    search = request.GET.get('search')
    sort_by = request.GET.get('sort_by')

    hotels = Hotel.objects.filter(is_active=True).select_related('hotel_owner').prefetch_related(
        Prefetch('hotel_images'),
        Prefetch('ameneties')
    )

    if search:
        hotels = hotels.filter(hotel_name__icontains=search)

    if sort_by == 'sort_low':
        hotels = hotels.order_by('hotel_offer_price')
    elif sort_by == 'sort_high':
        hotels = hotels.order_by('-hotel_offer_price')

    hotels = setImages(hotels)

    context = {'hotels': hotels}
    return render(request, 'index.html', context)

import math
def hotel_details_view(request, slug):
    today = date.today().isoformat()  # Format: YYYY-MM-DD
    try:
        hotel_details = Hotel.objects.prefetch_related('hotel_images', 'ameneties').get(hotel_slug=slug, is_active=True)
    except Hotel.DoesNotExist:
        messages.error(request, "Hotel not found or is no longer available.")
        return redirect('index')

    if request.method == "POST":
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        
        # Validate that dates are provided
        if not start_date or not end_date:
            messages.warning(request, "Please select both start and end dates for booking.")
            return HttpResponseRedirect(request.path_info)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            messages.warning(request, "Invalid date format. Please select valid dates.")
            return HttpResponseRedirect(request.path_info)
        
        # Validate that end date is after start date
        if end_date <= start_date:
            messages.warning(request, "End date must be after start date.")
            return HttpResponseRedirect(request.path_info)
        
        days_count = (end_date-start_date).days
        total_price = hotel_details.hotel_offer_price * days_count
        # Round to 2 decimal places for currency
        booking_price = round(total_price, 2)

        # Check if user is a HotelUser (not a vendor)
        try:
            booking_user = HotelUser.objects.get(id=request.user.id)
        except HotelUser.DoesNotExist:
            messages.error(request, "Only customers can book hotels. Vendors cannot make bookings.")
            return HttpResponseRedirect(request.path_info)

        # Check for overlapping bookings (same hotel, same user, overlapping dates)
        overlapping_bookings = HotelBooking.objects.filter(
            hotel=hotel_details,
            booking_user=booking_user
        ).filter(
            # Booking overlaps if: new_start <= existing_end AND new_end >= existing_start
            booking_start_date__lte=end_date,
            booking_end_date__gte=start_date
        )
        
        if overlapping_bookings.exists():
            messages.error(request, "You already have a booking for this hotel on the selected dates. Please choose different dates.")
            return HttpResponseRedirect(request.path_info)

        HotelBooking.objects.create(
            hotel = hotel_details,
            booking_user = booking_user,
            booking_start_date = start_date,
            booking_end_date = end_date,
            booking_price = booking_price
        )
        messages.success(request, "Booking is Successfull...")
        return redirect('my-bookings')

    context = {     
        'hotel_details':hotel_details,
        'today_date':today
    }
    return render(request, "hotel_details.html", context)

@login_required
def my_bookings_view(request):
    bookings = HotelBooking.objects.filter(booking_user=request.user).order_by('-booking_start_date')
    
    # Calculate booking days for each booking
    for booking in bookings:
        booking_start_date = str(booking.booking_start_date)
        booking_end_date = str(booking.booking_end_date)
        start_date = datetime.strptime(booking_start_date, '%Y-%m-%d')
        end_date = datetime.strptime(booking_end_date, '%Y-%m-%d')
        days_count = (end_date - start_date).days
        booking.total_booking_days = days_count
    
    context = {
        'bookings': bookings
    }
    return render(request, "my_bookings.html", context)

@login_required
def cancel_booking_view(request, booking_id):
    try:
        booking = HotelBooking.objects.get(id=booking_id, booking_user=request.user)
        hotel_name = booking.hotel.hotel_name
        booking.delete()
        messages.success(request, f"Booking for {hotel_name} has been cancelled successfully.")
    except HotelBooking.DoesNotExist:
        messages.error(request, "Booking not found or you don't have permission to cancel it.")
    
    return redirect('my-bookings')
