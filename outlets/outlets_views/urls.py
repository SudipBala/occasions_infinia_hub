
from django.urls import path

from outlets.outlets_views.views import OutletDetail, OutletCreate, OutletUpdate, OutletList

urlpatterns = [
    # path('create/', outlet_create_view, name="list_outlets")

    path('', OutletList.as_view(), name="list"),
    path('create/', OutletCreate.as_view(), name="create"),
    path('<int:id>/', OutletDetail.as_view(), name="detail"),
    path('<int:id>/update', OutletUpdate.as_view(), name='update'),
    # path('delete/<int:pk>', ItemDelete.as_view(), name='item_delete'),
]
