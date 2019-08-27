"""Occasions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path , include
from django.contrib.auth import views as auth_view

from delivery.views import SuperAdminListDelivery
from outlets.stock_views.views import SuperAdminListStock
from rest_framework import serializers, viewsets, routers


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register('v1/banner', BannerImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(('api.stocks_api.urls', 'stocks_api'), namespace='stocks_api')),
    path('api/', include(('api.outlets_api.urls', 'outlets_api'), namespace='outlets_api')),
    path('api/', include(('api.category_api.urls', 'category_api'), namespace='category_api')),
    path('api/v1/', include(('api.outletcart_api.urls', 'outletcart_api'), namespace='outlet_cart')),
    path('api/v1/', include(('api.category_api.urls', 'category_api'), namespace='category_api')),
    path('api/v1/', include(('api.delivery_api.urls', 'delivery_api'), namespace='delivery_api')),
    path('admin/', admin.site.urls),
    path('outlets/', include('outlets.urls', namespace="outlets")),
    path('category/', include(('outlets.category_views.urls', 'category'), namespace="category")),
    path('login/', auth_view.LoginView.as_view(), name='login'),
    path('logout/', auth_view.LogoutView.as_view(), name='logout'),
    path('stocks/', SuperAdminListStock.as_view(), name='admin_stock'),
    path('delivery/', SuperAdminListDelivery.as_view(), name="admin_delivery"),
    path('api/auth/', include('rest_framework.urls')),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2')),
    path('activity/', include(('actstream.urls', 'actstream'), namespace="activity")),
] +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

