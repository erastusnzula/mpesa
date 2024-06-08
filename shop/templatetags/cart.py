from django import template
from shop.models import Order

register = template.Library()


@register.filter
def cart_product_count(user):
    if user.is_authenticated:
        customer = user.customer
        order, created = Order.objects.get_or_create(customer=customer, is_complete=False)
        cart_items = order.get_cart_items
        if cart_items:
            return cart_items
        else:
            return 0
    else:
        order = {
            'get_cart_total': 0,
            'get_cart_items': 0,
            
        }
        cart_items=order['get_cart_items']
        if cart_items:
            return cart_items
        else:
            return 0
        