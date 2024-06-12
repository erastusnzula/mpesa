from django.urls import path 
from .views import StripePay

app_name = 'stripe'
urlpatterns = [
    path('', StripePay.as_view(), name='stripe-pay'),
]

