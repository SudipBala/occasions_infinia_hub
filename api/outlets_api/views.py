from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from api.outlets_api.serializers import OutletSerializer, OfferBannerSerializer
from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


class OutletListAPIView(ListAPIView):
    """
    API that allows outlets to be viewed or edited.
    """
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


class BannerImageAPIView(ListAPIView):
    """
    API that sends images for banner
    """
    queryset = OfferBannerModel.objects.all()
    serializer_class = OfferBannerSerializer
