from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('signup/', signup),

    path('login/', login_user, name='login_user'),
    path('login1/',login),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('productall/',ProductView, name='product-view'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('productadd/',product_add, name='product-add'),

    path('order/', create_order,name='create-order1'),
    path('order_create/', create_order_view, name='create-order'),

    path('seller/dashboard/', seller_dashboard, name='seller-dashboard'),
    path('buyer/dashboard/', buyer_dashboard, name='buyer-dashboard'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)