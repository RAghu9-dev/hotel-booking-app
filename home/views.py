from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import *
import random
from datetime import date, datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.db.models import Prefetch
# Create your views here.

def setImages(hotels):
    shared_images = list(HotelImages.objects.filter(hotel_id=109))
    for hotel in hotels:
        if shared_images:
            random_image = random.choice(shared_images)
            hotel.image_url = random_image.image.url
        else:
            hotel.image_url = None
    return hotels


@login_required
@cache_page(60*2)
# def index(request):
#     hotels = Hotel.objects.all().select_related('hotel_owner')
#       # You can set a default image in template if needed
#     search = request.GET.get('search')
#     if search:
#         total_hotels = hotels.filter(hotel_name__icontains = search)
#         hotels = setImages(total_hotels)
#     sort_by = request.GET.get('sort_by')
#     if sort_by:
#         if sort_by == 'sort_low':
#             hotels = hotels.order_by('hotel_offer_price')

#         elif sort_by == 'sort_high':
#             hotels = hotels.order_by('-hotel_offer_price')

#     hotels = setImages(hotels)
#     context = {'hotels': hotels}
#     return render(request, 'index.html', context)

def index(request):
    search = request.GET.get('search')
    sort_by = request.GET.get('sort_by')

    hotels = Hotel.objects.select_related('hotel_owner').prefetch_related(
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
    hotel_details = Hotel.objects.get(hotel_slug = slug)

    if request.method == "POST":
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        days_count = (end_date-start_date).days

        HotelBooking.objects.create(
            hotel = hotel_details,
            booking_user = HotelUser.objects.get(id = request.user.id),
            booking_start_date = start_date,
            booking_end_date = end_date,
            booking_price = math.floor(hotel_details.hotel_offer_price * days_count)
        )
        messages.success(request, "Booking is Successfull...")
        return redirect('index')

    context = {     
        'hotel_details':hotel_details,
        'today_date':today
    }
    return render(request, "hotel_details.html", context)
