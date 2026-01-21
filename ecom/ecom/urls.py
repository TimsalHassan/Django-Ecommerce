from django.contrib import admin
from django.urls import path,include
from .settings import base
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('product/', include('products.urls')),
    path('user/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
] + static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
