
from django.urls import path

from outlets.outlets_views.views import OutletsCreateView, ItemList, ItemDetail, ItemCreate, ItemUpdate, \
    ItemDelete, outlet_list_view

urlpatterns = [
    # path('create/', outlet_create_view, name="list_outlets")

    path('create/', OutletsCreateView.as_view(), name="create_outlets"),
    path('outlets/', outlet_list_view),
    path('item/', ItemList.as_view(), name='item_list'),
    path('item/<int:pk>', ItemDetail.as_view(), name='item_detail'),
    path('create/', ItemCreate.as_view(), name='item_create'),
    path('update/<int:pk>', ItemUpdate.as_view(), name='item_update'),
    path('delete/<int:pk>', ItemDelete.as_view(), name='item_delete'),
]