from django.urls import path

from outlets.stock_views.views import ListStock, DetailStock, AddStock, AddItem

app_name = 'stocks'

urlpatterns = [
    path('', ListStock.as_view(), name="list"),
    path('list/', ListStock.as_view(), name="list"),
    path('create/', AddStock.as_view(), name="create"),
    path('add-item/', AddItem.as_view(), name="add_item"),
    path('<int:pk>/', DetailStock.as_view(), name="detail"),
]