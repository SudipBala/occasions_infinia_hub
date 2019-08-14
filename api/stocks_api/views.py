from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.stocks_api.serializers import StocksListSerializer, StocksDetailSerializer
from outlets.stock_models import OutletStock


class StocksListAPIView(ListAPIView):
    queryset = OutletStock.objects.all()
    serializer_class = StocksListSerializer


class StocksDetailApiView(RetrieveAPIView):
    queryset = OutletStock.objects.all()
    serializer_class = StocksDetailSerializer
