from django.urls import path
from .views import DeliveryPolicyAPIView, TrackingDetailsAPIView, OutletOrderDetailsAPIView

app_name='delivery_api'
urlpatterns=[
    path('deliverypolicy/', DeliveryPolicyAPIView.as_view(), name='delivery_policy'),
    path('trackingdetails/', TrackingDetailsAPIView.as_view(), name='tracking_details'),
    path('outletorderdetails/',OutletOrderDetailsAPIView.as_view(), name='outler_order_details' )
]