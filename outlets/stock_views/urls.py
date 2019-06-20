from django.urls import path

from outlets.stock_views.views import ListStock, DetailStock

app_name = 'stocks'

urlpatterns = [
    path('', ListStock.as_view(), name="list"),
    path('list/', ListStock.as_view(), name="list"),
    # path('create/', CreateStock.as_view(), name="create"),
    path('<int:pk>/', DetailStock.as_view(), name="detail"),
]