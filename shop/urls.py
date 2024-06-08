from django.urls import path
from .views import ProductList, AddToCart, Cart

app_name='shop'
urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('add_to_cart/', AddToCart.as_view(), name='add-to-cart'),
    path('cart/', Cart.as_view(), name='cart'),
]
