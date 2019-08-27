from rest_framework import serializers
from outlets.models import OutletCart

class OutletCartSerializer(serializers.ModelSerializer):

    class Meta:
        model= OutletCart
        fields=[
            'id',
            'itemline',
            'associated_user',
            'checked_out'
        ]
