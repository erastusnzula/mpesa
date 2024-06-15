from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views import View
from django.http import JsonResponse
from .models import Product, Order, OrderItem, ShippingAddress
import datetime
from .templatetags.cart import update_cart_items
from .utils import cookies_cart, cart_data



class ProductList(View):
    def get(self,request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            cookieData = cookies_cart(request)
           
        products = Product.objects.all()
        context = {'products': products}
        return render(self.request, 'shop/product_list.html', context)
    
class ProductDetail(View):
    def get(self, request, id):
        if not self.request.user.is_authenticated:
            cookieData = cookies_cart(request)
        product = Product.objects.get(id=id)
        context = {'product': product}
        return render(request, 'shop/product_details.html', context)

class AddToCart(View):
    def get(self,request,  *args, **kwargs):
        data = cart_data(request)
        items = data['items']
        order = data['order']
            
        context = {'items': items, 'order': order}
        return render(self.request, 'shop/cart.html', context)
    
    
    def post(self, *args, **kwargs):
        data = json.loads(self.request.body)
        product_id = data['product_id']
        action = data['action']
        print(product_id, action)
        customer = self.request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()
        print(orderItem)
        if orderItem.quantity <= 0:
            orderItem.delete()
        return JsonResponse("item added successfully to cart.", safe=False)
    
class Checkout(View):
    def get(self, request,*args, **kwargs):
        data = cart_data(request)
        items = data['items']
        order = data['order']
        context = {'items': items,'order': order}
        return render(self.request, 'shop/checkout.html', context)
    
    def post(self, request):
        data = json.loads(request.body)
        transaction_id = datetime.datetime.now().timestamp()
        print(data['payWith'])
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
            total = float(data['userData']['total'])
            order.transaction_id = transaction_id
            if total == order.get_cart_total:
                order.is_complete = True
            order.save()
            
            if order.for_shipping == True:
                ShippingAddress.objects.create(
                    customer = customer,
                    order = order,
                    address = data['shippingInformation']['address'],
                    city = data['shippingInformation']['city'],
                    country = data['shippingInformation']['country'],
                    zipcode = data['shippingInformation']['zipCode']
                )
                
        else:
            print("User not logged in.")
            
        return JsonResponse("Payment complete.", safe=False)