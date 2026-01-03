from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q
from django.contrib import messages 
from accounts.models import HotelUser, HotelVendor, Hotel, Ameneties, HotelImages, HotelBooking
from .templates.utils.sendEmail import send_test_email, generateToken, send_email_with_otp, generate_slug
from django.contrib.auth import authenticate, login, logout
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

def login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        password = request.POST.get('password')

        hotel_user = HotelUser.objects.filter(email = user_email)
        if not hotel_user:
            messages.warning(request, "Incorrect email address")
            return redirect("/accounts/login/")
        
        if not hotel_user[0].is_verified:
            messages.warning(request, "Please verify your account, Check your email inbox.")
            return redirect("/accounts/login/")

        user = authenticate(request, username = hotel_user[0].username, password=password)
        if not user:
            print("authentication failed")
            messages.warning(request, "Incorrect password")
            return redirect("/accounts/login/")
        login(request, user)
        return redirect("/")    
    return render(request, 'login.html')

def login_with_otp_view(request):
    context = {
        "show_email":True,
        "show_otp":True,
        "display_otp":"d-none",
        "display":None,
        "email":""
    }
    return render(request, "login_otp.html", context)

def login_otp_enter_view(request, email):
    hotel_user = HotelUser.objects.filter(email = email)
    if not hotel_user:
        messages.warning(request, "Invalid email address, Please register if not..")
        return redirect("/accounts/login/")
    otp = random.randint(1111, 9999)
    hotel_user = HotelUser.objects.get(email=email)
    hotel_user.otp = otp
    hotel_user.save()
    send_email_with_otp(email, otp)
    context = {
        "show_email":False,
        "show_otp":True,
        "display":"d-none",
        "display_otp":"d-block",
        "email":email
    }
    return render(request, "login_otp.html", context)

def verify_otp_view(request, email, otp):
    hotel_user = HotelUser.objects.get(email=email)
    if str(hotel_user.otp) != str(otp):
        messages.warning(request, "Wrong OTP, re-enter correct OTP")
        context = {
            "show_email": False,
            "show_otp": True,
            "display": "d-none",
            "display_otp": "d-block",
            "email": email
        }
        return render(request, "login_otp.html", context)
    login(request, hotel_user)
    return redirect("/")
    
def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        hotel_user = HotelUser.objects.filter(
            Q(email=email) | Q(username=phone_number) 
        )
        if hotel_user:
            messages.warning(request, "An account exists with this email or phone try another one")
            return redirect('/accounts/register/')
        
        hotel_user = HotelUser.objects.create(
            username = phone_number,
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone_number = phone_number,
            email_token = generateToken()
        )
        hotel_user.set_password(password)
        hotel_user.save()
        send_test_email(hotel_user.email, hotel_user.email_token)
        messages.success(request, f"A verification email sent to you registered email:{hotel_user.email}")

    return render(request, 'register.html')
    
def verify_email_view(request, token):
    try:
        hotel_user = None
        user = False
        vendor = False

        try:
            hotel_user = HotelUser.objects.get(email_token=token)
            user = True
        except HotelUser.DoesNotExist:
            try:
                hotel_user = HotelVendor.objects.get(email_token=token)
                vendor = True
            except HotelVendor.DoesNotExist:
                return HttpResponse("Invalid Token")

        hotel_user.is_verified = True
        hotel_user.save()

        if user:
            messages.success(request, "Email successfully verified")
            return redirect('/accounts/login/')
        elif vendor:
            messages.success(request, "Email successfully verified")
            return redirect('/accounts/vendor-login/')

    except Exception as e:
        return HttpResponse("Something went wrong")

def vendor_login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            vendor = HotelVendor.objects.get(email=user_email)
        except HotelVendor.DoesNotExist:
            messages.warning(request, "Incorrect email address")
            return redirect("/accounts/vendor-login/")

        if not vendor.is_verified:
            messages.warning(
                request,
                "Please verify your account. Check your email inbox."
            )
            return redirect("/accounts/vendor-login/")

        user = authenticate(
            request,
            username=vendor.username,
            password=password
        )

        if user is None:
            messages.warning(request, "Incorrect password")
            return redirect("/accounts/vendor-login/")

        login(request, user)
        return redirect("/accounts/vendor-dashboard/")

    return render(request, 'vendor/vendor_login.html')

def vendor_register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        business_name = request.POST.get('business_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')

        if HotelVendor.objects.filter(
            Q(username=phone_number) |
            Q(email=email) |
            Q(phone_number=phone_number)
        ).exists():
            messages.warning(
                request,
                "An account already exists with this email or phone number"
            )
            return redirect('/accounts/vendor-register/')

        hotel_user = HotelVendor.objects.create_user(
            username=phone_number,     # MUST be unique
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            business_name=business_name,
        )

        hotel_user.email_token = generateToken()
        hotel_user.save()

        send_test_email(hotel_user.email, hotel_user.email_token)

        messages.success(
            request,
            f"A verification email has been sent to {hotel_user.email}"
        )
        return redirect('/accounts/vendor-login/')

    return render(request, 'vendor/vendor_register.html')


def setImages(hotels):
    shared_images = list(HotelImages.objects.filter(hotel_id=109))
    for hotel in hotels:
        if shared_images:
            random_image = random.choice(shared_images)
            hotel.image_url = random_image.image.url
        else:
            hotel.image_url = None
    return hotels

@login_required(login_url="/accounts/vendor-login/")
def vendor_dashboard_view(request):
    hotels = Hotel.objects.filter(hotel_owner = request.user.id)
    hotels = setImages(hotels)
    context = {
        'hotels':hotels[:10]
    }
    return render(request, "vendor/vendor_dashboard.html", context)

def add_hotel_view(request):
    if request.method == 'POST':
        hotel_name = request.POST.get('name')
        hotel_description = request.POST.get('description')
        ameneties_ids = request.POST.getlist('ameneties')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('location')
        hotel_slug = generate_slug(hotel_name)

        try:
            hotel_vendor = request.user.hotelvendor
        except HotelVendor.DoesNotExist:
            messages.error(request, "Only vendors can add hotels.")
            return redirect("/")

        hotel_obj = Hotel.objects.create(
            hotel_name=hotel_name,
            hotel_description=hotel_description,
            hotel_slug=hotel_slug,
            hotel_owner=hotel_vendor,
            hotel_price=hotel_price,
            hotel_offer_price=hotel_offer_price,
            hotel_location=hotel_location,
        )
        amenities = Ameneties.objects.filter(id__in=ameneties_ids)
        hotel_obj.ameneties.add(*amenities)

        messages.success(request, "Hotel created successfully")
        return redirect("add-hotel")

    ameneties = Ameneties.objects.all()
    context = {
        "hotel_ameneties": ameneties
    }
    return render(request, "vendor/add_hotel.html", context)

@login_required(login_url="/accounts/vendor-login/")
def upload_images_view(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.method == 'POST':
        image = request.FILES['image']
        HotelImages.objects.create(
            hotel = hotel_obj,
            image = image
        )
        print(image)

        return HttpResponseRedirect(request.path_info)
    return render(request, "vendor/upload_image.html", context = {'images' : hotel_obj.hotel_images.all()})

@login_required(login_url="/accounts/vendor-login/")
def delete_images_view(request, id):
    hotel_image_obj = HotelImages.objects.filter(id = id)
    if hotel_image_obj:
        hotel_image_obj[0].delete()
        return HttpResponseRedirect(request.path_info)
    return HttpResponseRedirect("/accounts/vendor-dashboard/")

@login_required(login_url="/accounts/vendor-login/")
def edit_hotel_view(request, slug):
    hotel_obj = Hotel.objects.get(hotel_slug = slug)
    if request.user.id != hotel_obj.hotel_owner.id:
        return HttpResponse("You are not authorized")
    
    if request.method == 'POST':
        hotel_name = request.POST.get('name')
        hotel_description = request.POST.get('description')
        print("this is description: ", hotel_description)
        ameneties = request.POST.getlist('ameneties')
        hotel_price = request.POST.get('hotel_price')
        hotel_offer_price = request.POST.get('hotel_offer_price')
        hotel_location = request.POST.get('location')

        hotel_obj.hotel_name = hotel_name
        hotel_obj.hotel_description = hotel_description
        hotel_obj.hotel_price = hotel_price
        hotel_obj.hotel_offer_price = hotel_offer_price
        hotel_obj.hotel_location = hotel_location
        hotel_obj.save()   

        messages.success(request, "Hotel Details Updated")
        return HttpResponseRedirect(request.path_info)
    
    hotel_ameneties = Ameneties.objects.all()
    context = {
        'hotel_obj' : hotel_obj,
        'hotel_ameneties':hotel_ameneties
    }
    
    return render(request, "vendor/edit_hotel_details.html", context)

from datetime import date, datetime
def view_bookings_view(request):
    bookings = HotelBooking.objects.all()
    vendor_bookings = []
    for booking in bookings:
        hotel = booking.hotel
        if hotel.hotel_owner.id == request.user.id:
            booking_start_date = str(booking.booking_start_date)
            booking_end_date = str(booking.booking_end_date)
            start_date = datetime.strptime(booking_start_date, '%Y-%m-%d')
            end_date = datetime.strptime(booking_end_date, '%Y-%m-%d')
            days_count = (end_date-start_date).days
            booking.total_booking_days = days_count
            vendor_bookings.append(booking)
    context = {
        'bookings':vendor_bookings
    }
    return render(request, "vendor/view_bookings.html", context)





    
    