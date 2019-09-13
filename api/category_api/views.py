from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from outlets.category_models import Category
from outlets.stock_models import BaseItem, OutletItem
from .serializers import CategoryListSerializer, CategoryDetailItemSerializer, ItemSerializer


class CategoryList(ListAPIView):
    # queryset = Category.objects.get_categories()
    # serializer_class = CategoryListSerializer
    def get(self, request, *args, **kwargs):
        category = Category.objects.get_categories()
        serializer = CategoryListSerializer(category, many=True)
        return Response({"message": "Listed Outlets", "status": status.HTTP_200_OK, "data": serializer.data})


# class SubCategoryList(ListAPIView):
#     queryset = Category.objects.get_sub_categories()
#     serializer_class = CategorySerializer


class CategoryDetail(RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        category_id = self.kwargs['pk']
        category = Category.objects.filter(id=category_id,level=0)

        if category:
            serializer = CategoryListSerializer(category, many=True)
            return Response({"message": "Category Details", "status":status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"message": "Category Not found", "status":status.HTTP_404_NOT_FOUND})


class CategoryItemsList(ListAPIView):
    """
    List all the items in a particular category
    """

    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        baseitem = BaseItem.objects.filter(outletitem__type1=category)
        if baseitem:
            serializer = CategoryDetailItemSerializer(baseitem, many=True)
            return Response({"message": "Item Lists", "status": status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"message": "Items Not found", "status": status.HTTP_404_NOT_FOUND})


class ItemDetails(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        outletitem = BaseItem.objects.filter(outletitem__type1=category, id=self.kwargs['item_pk'])
        if outletitem:
            serializer = ItemSerializer(outletitem, many=True)
            return Response({"message": "Item ", "status": status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"message": "Item Not found", "status": status.HTTP_404_NOT_FOUND})


















