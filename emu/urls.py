
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mpesa/', include('mpesa.urls'), name='mpesa'),
    path('paypal/', include('paypal.urls'), name='paypal'),
    path('stripe/', include('stripe.urls'), name='stripe'),
    path('shop/', include('shop.urls'), name='shop'),
    path('', include('dashboard.urls'), name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
