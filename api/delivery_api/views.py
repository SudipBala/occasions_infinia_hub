from rest_framework import generics
from .serializer import DeliveryPolicySerailizer, TrackingDetailsSerializer, OutletOrderDetailsSerializer
from delivery.models import DeliveryPolicy, TrackingDetails, OutletOrderDetails

class DeliveryPolicyAPIView(generics.ListAPIView):
    queryset = DeliveryPolicy.objects.all()
    serializer_class = DeliveryPolicySerailizer

class TrackingDetailsAPIView(generics.ListAPIView):
    queryset = TrackingDetails.objects.all()
    serializer_class = TrackingDetailsSerializer

class OutletOrderDetailsAPIView(generics.ListAPIView):
    queryset = OutletOrderDetails.objects.all()
    serializer_class = OutletOrderDetailsSerializer

