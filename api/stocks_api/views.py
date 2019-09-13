from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.stocks_api.serializers import StocksListSerializer, StocksDetailSerializer
from outlets.stock_models import OutletStock


class StocksListAPIView(ListAPIView):
    # queryset = OutletStock.objects.all()
    # serializer_class = StocksListSerializer
    def get(self, request, *args, **kwargs):
        outlet_stocks = OutletStock.objects.all()
        serializer = StocksListSerializer(outlet_stocks, many=True)
        return Response({"message": "Stocks List", "status": status.HTTP_200_OK, "data": serializer.data})


class StocksDetailApiView(RetrieveAPIView):
    # queryset = OutletStock.objects.all()
    # serializer_class = StocksDetailSerializer
    def retrieve(self, request, *args, **kwargs):
        stock_id = self.kwargs['pk']
        stock_detail = OutletStock.objects.filter(id=stock_id)
        if stock_detail:
            serializer = StocksDetailSerializer(stock_detail, many=True)
            return Response({"message": "Stock Detail", "status": status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"message": "Stocks List", "status": status.HTTP_404_NOT_FOUND})





