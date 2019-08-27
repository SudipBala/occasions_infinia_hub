from rest_framework import generics

from outlets.category_models import Category
from .serializers import CategorySerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.get_categories()
    serializer_class = CategorySerializer

class SubCategoryList(generics.ListAPIView):
    queryset = Category.objects.get_sub_categories()
    serializer_class = CategorySerializer






