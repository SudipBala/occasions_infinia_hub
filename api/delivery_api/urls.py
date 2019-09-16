from django.urls import path
from .views import DeliveryPolicyAPIView, TrackingDetailsAPIView, OutletOrderDetailsAPIView

app_name='delivery_api'

urlpatterns=[
    path('v1/deliverypolicy/', DeliveryPolicyAPIView.as_view(), name='delivery_policy'),
    path('v1/trackingdetails/', TrackingDetailsAPIView.as_view(), name='tracking_details'),
    path('v1/outletorderdetails/',OutletOrderDetailsAPIView.as_view(), name='outler_order_details' )
]