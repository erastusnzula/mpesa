from django.shortcuts import render
from django.views import View

class CreatePayment(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'paypal/create_payment.html')
