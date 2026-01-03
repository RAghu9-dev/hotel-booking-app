
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug>/hotel-details', views.hotel_details_view, name="hotel-details")
]
