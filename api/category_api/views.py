from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView

from outlets.category_models import Category
from outlets.stock_models import BaseItem, OutletItem
from .serializers import CategoryListSerializer, CategoryDetailItemSerializer, ItemSerializer


class CategoryList(ListAPIView):
    queryset = Category.objects.get_categories()
    serializer_class = CategoryListSerializer

# class SubCategoryList(ListAPIView):
#     queryset = Category.objects.get_sub_categories()
#     serializer_class = CategorySerializer


class CategoryDetail(ListAPIView):
    serializer_class = CategoryListSerializer

    def get_queryset(self):
        category=get_object_or_404(Category, level=0, pk=self.kwargs['pk'])
        return category.children.all()


class CategoryItemsList(ListAPIView):
    """
    List all the items in a particular category
    """
    serializer_class = CategoryDetailItemSerializer

    def get_queryset(self, **kwargs):
        category=get_object_or_404(Category, pk=self.kwargs['category_pk'])
        baseitem = BaseItem.objects.filter(outletitem__type1=category).values('display_name', 'quantity', 'image')
        return baseitem


class ItemDetails(ListAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        category=get_object_or_404(Category, pk=self.kwargs['category_pk'])
        outletitem= BaseItem.objects.filter(outletitem__type1=category, id=self.kwargs['item_pk']).values()
        return outletitem















