from django.shortcuts import render, redirect, get_object_or_404
import json
from django.views import View
from django.http import JsonResponse
from .models import Product, Order, OrderItem, ShippingAddress
import datetime
from .templatetags.cart import update_cart_items


def cookies_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print(f"Cart {cart}")
    items = []
    order = {'get_cart_total': 0,'get_cart_items': 0,'for_shipping': False, 'total': 0}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]["quantity"])
            order['total'] = total
            order['get_cart_total'] += total
            order['get_cart_items'] +=  cart[i]["quantity"]
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'get_image_url': product.get_image_url
                },
                'quantity': cart[i]["quantity"], 
                'get_total': total
                }
            items.append(item)
            if product.is_digital == False:
                order['for_shipping'] = True
            update_cart_items.items =cartItems
            
        except:
            pass
    return {'items': items, 'order': order, 'total': order['total']}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        items = order.orderitem_set.all()
    else:
        cookieData = cookies_cart(request)
        items = cookieData['items']
        order = cookieData['order']
    return {'items': items, 'order': order}