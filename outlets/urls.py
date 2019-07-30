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

from django.urls import path, include

app_name = 'outlets'

urlpatterns = [
    path('', include(('outlets.outlets_views.urls', 'outlets'), namespace="outlet")),
    path('<int:outlet_id>/stocks/', include(('outlets.stock_views.urls', 'outlets'), namespace="stocks")),
    path('<int:outlet_id>/delivery/', include(('delivery.deliverypolicy_views.urls', 'delivery'), namespace="delivery")),
    path('<int:outlet_id>/orders/', include(('delivery.order_views.urls', 'delivery'), namespace="orders"))
]
