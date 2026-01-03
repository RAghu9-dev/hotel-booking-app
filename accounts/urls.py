from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login-with-otp/', views.login_with_otp_view, name="login-otp-page"),
    path('login-with-otp/<str:email>/', views.login_otp_enter_view, name="login-otp-enter" ),
    path('<str:email>/verify-otp/<int:otp>/',views.verify_otp_view, name="verify-otp" ),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('verify-account/<token>', views.verify_email_view, name='verify-account'),

    # Vendor routes - keep these before dynamic slug patterns
    path('vendor-login/', views.vendor_login_view, name="vendor-login"),
    path('vendor-register/', views.vendor_register_view, name="vendor-register"),
    path('vendor-dashboard/', views.vendor_dashboard_view, name="vendor-dashboard"),
    path('add-hotel/', views.add_hotel_view, name="add-hotel"),
    path('view-bookings/', views.view_bookings_view, name='view-bookings'),
    
    # Dynamic routes - keep these at the end
    path('<slug>/upload-image', views.upload_images_view, name="upload-image"),
    path('<id>/delete-image/', views.delete_images_view, name="delete-image"),
    path('<slug>/edit-hotel-details/', views.edit_hotel_view, name='edit-hotel'),
]
