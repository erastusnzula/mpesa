from django.shortcuts import render
from django.views import View
from shop.models import Product, Order, OrderItem, ShippingAddress, Customer
import datetime
from shop.templatetags.cart import update_cart_items
from shop.utils import cookies_cart, cart_data, guest_order
import json
from django.http import JsonResponse

class CreatePayment(View):
    def get(self,request, *args, **kwargs):
        data = cart_data(request)
        items = data['items']
        order = data['order']
        context = {'items': items,'order': order}
        return render(self.request, 'paypal/create_payment.html', context)
    
    def post(self, request):
        data = json.loads(request.body)
        if request.user.is_authenticated:
            customer = request.user.customer
            order = Order.objects.get(customer=customer, is_complete=False)  
            print(order)   
                
        else:
            print("Not logged in")
           
        order.is_complete = True
        update_cart_items.items = 0
        order.save()  
        return JsonResponse("Payment complete.", safe=False)
