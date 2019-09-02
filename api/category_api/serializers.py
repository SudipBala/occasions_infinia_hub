from rest_framework import serializers

from outlets.category_models import Category
# from api.stocks_api.serializers import ItemSerializer
from outlets.stock_models import OutletItem, BaseItem

"""
serailizers for stock_models and category_models
"""


class CategoryListSerializer(serializers.ModelSerializer):
    """ read only serializer """
    class Meta:
        model = Category
        fields = ['id', 'level', 'category_name', 'parent', 'image', 'disabled']


class CategoryDetailItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseItem
        fields = ['display_name', 'quantity', 'image']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=BaseItem
        fields='__all__'










