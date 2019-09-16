from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.outlets_api.serializers import OutletSerializer
from libs.constants import COUNTRY_CHOICES
from outlets.outlet_models import Outlet


class CountryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = [{'value': item[1]} for item in COUNTRY_CHOICES]
        return Response({"message": "Country List", "status":status.HTTP_200_OK,"data":data})


class CountryOutletAPIView(ListAPIView):

    def get(self, request, *args, **kwargs):
        country_name = self.kwargs.get('country')
        outlets = Outlet.objects.filter(country=country_name)
        serializer = OutletSerializer(outlets, many= True)
        return Response({"message": "Country Outlets", "status":status.HTTP_200_OK, "data":serializer.data})

