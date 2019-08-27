from django.urls import path
from .views import CategoryList, SubCategoryList


app_name='category_api'
urlpatterns=[
    path('category/', CategoryList.as_view(), name= 'category_list'),
    # path('category/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('category/<int:level>/', SubCategoryList.as_view(), name='subacategory_list'),
]