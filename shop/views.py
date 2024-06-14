from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views import View
from django.http import JsonResponse
from .models import Product, Order, OrderItem
import datetime

class ProductList(View):
    def get(self, *args, **kwargs):
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(self.request, 'shop/product_list.html', context)
    
class ProductDetail(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        context = {
            'product': product
        }
        return render(request, 'shop/product_details.html', context)

class AddToCart(View):
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
            items = order.orderitem_set.all()
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart = {}
            print(cart)
            items = []
            order = {
                'get_cart_total': 0,
                'get_cart_items': 0,
                'for_shipping': False
            }
        context = {
            'items': items,
            'order': order
        }
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
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = self.request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
            items = order.orderitem_set.all()
        else:
            try:
                cart = json.loads(self.request.COOKIES['cart'])
            except:
                cart = {}
            print(cart)
            items = []
            order = {
                'get_cart_total': 0,
                'get_cart_items': 0,
                'for_shipping': False
            }
        context = {
            'items': items,
            'order': order
        }
        return render(self.request, 'shop/checkout.html', context)
    
    def post(self, request):
        data = json.loads(request.body)
        transaction_id = datetime.datetime.now().timestamp()
        print(data['payWith'])
        if request.user.is_authenticated:
            print(f"User {self.request.user.customer}")
        return JsonResponse("Payment complete.", safe=False)