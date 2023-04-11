from django.urls import path
from .views import *
from appointment.views import *

app_name = "accounts"

urlpatterns = [
    path('customer/registration', RegisterCustomerView.as_view(), name='customer-registration'),
    path('customer/profile-update', EditCustomerProfileView.as_view(), name='customer-profile-update'),
    path('serviceman/registration', RegisterservicemanView.as_view(), name='serviceman-registration'),
    path('serviceman/profile-update', EditservicemanProfileView.as_view(), name='serviceman-profile-update'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]