from rest_framework import viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView

from api.outlets_api.serializers import OfferBannerSerializer, OutletDetailSerializer, OutletSerializer
from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


class OutletListAPIView(ListAPIView):
    """
    API that allows outlets to be viewed only.
    """
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


class BannerImageAPIView(ListAPIView):
    """
    API that sends images for banner
    """
    queryset = OfferBannerModel.objects.all()
    serializer_class = OfferBannerSerializer


class OutletDetailAPIView(RetrieveAPIView):
    queryset = Outlet.objects.all()
    serializer_class = OutletDetailSerializer


