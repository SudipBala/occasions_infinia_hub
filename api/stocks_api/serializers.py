from rest_framework.serializers import ModelSerializer

from outlets.stock_models import OutletStock, BaseItem


class ItemSerializer(ModelSerializer):
    class Meta:
        model = BaseItem
        fields = "__all__"


class StocksListSerializer(ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OutletStock
        fields = [
            'item',
            'price',
            'currency'
        ]


class StocksDetailSerializer(ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = OutletStock
        fields = "__all__"
