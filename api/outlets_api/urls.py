from django.urls import path

from api.outlets_api.views import OutletListAPIView, BannerImageAPIView, OutletDetailAPIView, OutletStockAPIView

app_name = 'outlets_api'

urlpatterns = [
    path('v1/outlets/', OutletListAPIView.as_view(), name="outlets_list"),
    path('v1/banners/', BannerImageAPIView.as_view(), name="outlets_list"),
    path('v1/outlets/<int:pk>/', OutletDetailAPIView.as_view(), name="outlets_detail"),
    path('v1/outlets/<int:outlet_id>/stocks/', OutletStockAPIView.as_view(), name="stocks"),
]
