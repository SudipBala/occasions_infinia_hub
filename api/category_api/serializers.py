from rest_framework import serializers

from outlets.category_models import Category
from outlets.stock_models import BaseItem, OutletItem, OutletStock
# from outlets.stock_models import PriceModifiers

"""
serailizers for stock_models and category_models
"""
class CategorySerializer(serializers.ModelSerializer):
    """ read only serializer """
    class Meta:
        model = Category
        fields = ['id', 'level', 'category_name', 'parent']




