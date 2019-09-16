from django.urls import path
from .views import CategoryList, CategoryDetail, CategoryItemsList, ItemDetails

app_name='category_api'
urlpatterns=[
    path('v1/category/', CategoryList.as_view(), name= 'category_list'),
    path('v1/category/<pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('v1/category/<category_pk>/items/', CategoryItemsList.as_view(), name='category_detail'),
    path('v1/category/<category_pk>/items/<item_pk>/', ItemDetails.as_view(), name='item_detail'),
    # path('<pk>/items/', ItemDetails.as_view())
    # path('subcategory/', SubCategoryList.as_view(), name='subacategory_list'),
    # path('items/', ItemsInCategory.as_view(), name='items' ),


]