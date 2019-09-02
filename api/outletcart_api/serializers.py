from rest_framework import serializers

from api.stocks_api.serializers import StocksDetailSerializer
from outlets.models import OutletCart, OutletItemLine


class ItemLineSerializer(serializers.ModelSerializer):
    stocked_item = StocksDetailSerializer()

    class Meta:
        model = OutletItemLine
        fields = '__all__'


class OutletCartSerializer(serializers.ModelSerializer):
    itemline = ItemLineSerializer(many=True)

    class Meta:
        model = OutletCart
        fields = "__all__"
