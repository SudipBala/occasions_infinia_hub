from rest_framework import viewsets

from api.outlets_api.serializers import OutletSerializer, OfferBannerSerializer
from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


class OutletViewSet(viewsets.ModelViewSet):
    """
    API that allows outlets to be viewed or edited.
    """
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


class BannerImageViewSet(viewsets.ModelViewSet):
    """
    API that sends images for banner
    """
    queryset = OfferBannerModel.objects.all()
    serializer_class = OfferBannerSerializer
