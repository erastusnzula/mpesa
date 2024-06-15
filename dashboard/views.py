from django.shortcuts import render
from django.views import View
from shop.models import Order
from shop.utils import cookies_cart

class Index(View):
    def get(self,request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            cookieData = cookies_cart(request)
        return render(self.request, 'dashboard/index.html')
