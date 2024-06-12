from django.shortcuts import render
from django.views import View


class StripePay(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'stripe/stripe_pay.html')
