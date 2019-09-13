from rest_framework.renderers import BaseRenderer
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.outlets_api.serializers import OfferBannerSerializer, OutletDetailSerializer, OutletSerializer
from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


# class OutletListAPIView(ListAPIView):
#     """
#     API that allows outlets to be viewed only.
#     """
#     permission_classes = (IsAuthenticated, )
#     queryset = Outlet.objects.all()
#     serializer_class = OutletSerializer
class OutletListAPIView(ListAPIView):

    # permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        outlets = Outlet.objects.all()
        serializer = OutletSerializer(outlets, many=True)
        return Response({"message": "Listed Outlets", "status": status.HTTP_200_OK, "data": serializer.data})


class BannerImageAPIView(ListAPIView):
    """
    API that sends images for banner
    """
    # queryset = OfferBannerModel.objects.all()
    # serializer_class = OfferBannerSerializer
    def get(self, request, *args, **kwargs):
        banners = OfferBannerModel.objects.all()
        serializer = OfferBannerSerializer(banners, many=True)
        return Response({"message": "Offers And Banners List", "status": status.HTTP_200_OK, "data": serializer.data})


class OutletDetailAPIView(RetrieveAPIView):
    # outlet_id = self.kwargs['outlet_id']  # use <outlet_id> passed in url
    # return OutletStock.objects.filter(outlet=outlet_id)

    def retrieve(self, request, *args, **kwargs):
        outlet_id = self.kwargs['pk']
        outlets = Outlet.objects.filter(id=outlet_id)
        if outlets:
            serializer = OutletDetailSerializer(outlets, many=True)
            return Response({"message": "Outlet Details", "status":status.HTTP_200_OK, "data": serializer.data})
        else:
            return Response({"message": "Outlet Not found", "status":status.HTTP_404_NOT_FOUND})



