from django.urls import path
from .views import ProductList, AddToCart, ProductDetail, Checkout

app_name='shop'
urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('add_to_cart/', AddToCart.as_view(), name='add-to-cart'),
    path('<int:id>/', ProductDetail.as_view(), name='product-details'),
    path('checkout/', Checkout.as_view(), name='checkout'),
]
