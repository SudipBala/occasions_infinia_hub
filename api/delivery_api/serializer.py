"""
contains serializer for delviery.models
"""

from rest_framework import serializers
from delivery.models import  DeliveryPolicy, TrackingDetails, OutletOrderDetails

class DeliveryPolicySerailizer(serializers.ModelSerializer):
    class Meta:
        model=DeliveryPolicy
        fields=['id', 'outlet', 'radius', 'price', 'currency', 'delivery_time']

class TrackingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model= TrackingDetails
        exclude=[]

class OutletOrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model= OutletOrderDetails
        fields=['id', 'order_number', 'trackers']

