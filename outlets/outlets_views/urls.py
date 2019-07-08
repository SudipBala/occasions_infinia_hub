
from django.urls import path

from outlets.outlets_views.views import OutletDetail, OutletCreate, OutletUpdate, OutletList, OutletDelete

urlpatterns = [
    # path('create/', outlet_create_view, name="list_outlets")

    path('list/', OutletList.as_view(), name="list"),
    path('create/', OutletCreate.as_view(), name="create"),
    path('<int:id>/', OutletDetail.as_view(), name="detail"),
    path('<int:id>/update', OutletUpdate.as_view(), name='update'),
    path('<int:pk>/delete', OutletDelete.as_view(), name='delete')
]
