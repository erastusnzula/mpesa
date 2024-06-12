from django.urls import path
from .views import CreatePayment

app_name = 'paypal'
urlpatterns = [
    path('', CreatePayment.as_view(), name='create-payment')
]
