from django.urls import path

from api.stocks_api.views import StocksListAPIView, StocksDetailApiView

app_name = 'stocks_api'

urlpatterns = [
    path('v1/stocks/', StocksListAPIView.as_view(), name="stocks_list"),
    path('v1/stocks/<int:pk>/', StocksDetailApiView.as_view(), name="stocks_detail")
]
