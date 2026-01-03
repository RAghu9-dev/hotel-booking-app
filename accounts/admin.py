from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(HotelUser)
admin.site.register(HotelVendor)
admin.site.register(Ameneties)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name', 'hotel_owner', 'hotel_location', 'hotel_price', 'hotel_offer_price', 'is_active')
    list_filter = ('is_active', 'hotel_owner')
    search_fields = ('hotel_name', 'hotel_location', 'hotel_slug')
    readonly_fields = ('hotel_slug',)
    list_editable = ('is_active',)
    
@admin.register(HotelImages)
class HotelImagesAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')
    list_filter = ('hotel',)
    search_fields = ('hotel__hotel_name',)

@admin.register(HotelBooking)
class HotelBookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'booking_user', 'booking_start_date', 'booking_end_date', 'booking_price')
    list_filter = ('booking_start_date', 'booking_end_date')
    search_fields = ('hotel__hotel_name', 'booking_user__email', 'booking_user__first_name', 'booking_user__last_name')
    date_hierarchy = 'booking_start_date'