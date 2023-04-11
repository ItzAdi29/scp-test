"""
in_home_service URL Configuration

"""

from django.urls import path
from appointment.views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'appointment'

urlpatterns = [

    path('', HomePageView.as_view(), name='home'),
    path('home', HomePageView.as_view(), name='home'),
    path('service', ServiceView.as_view(), name='service'),
    path('search/', SearchView.as_view(), name='search'),
    path('query', query, name='query'),
    path('map_location', map_location, name='map_location'),
    path('serviceman/appointment-create', AppointmentCreateView.as_view(), name='serviceman-appointment-create'),
    path('serviceman/appointments/', AppointmentListView.as_view(), name='serviceman-appointments'),
    path('customer/servicemans-list', servicemanListView.as_view(), name='customer-servicemans-list'),
    path('customer/book-appointment', TakeAppointmentView.as_view(), name='customer-book-appointment'),
    path('customer/appointment-history', CustomerAppointmentHistoryListView.as_view(), name='customer-appointment-history'),
    path('serviceman/delete-appointment/id/<pk>', AppointmentDeleteView.as_view(), name='delete-appointment'),
    path('customer/delete-appointment/id/<pk>', CustomerDeleteAppointmentView.as_view(), name='delete-customer-appointment'),
    path('customer/update-appointment/id/<pk>', UpdateCustomerAppointmentView.as_view(), name='update-customer-appointment'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
