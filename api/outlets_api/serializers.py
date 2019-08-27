from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField
from rest_framework.validators import UniqueValidator

from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


class OfferBannerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferBannerModel
        fields = ['banner_image', 'offer_message', 'offer_discount']


class OutletSerializer(serializers.HyperlinkedModelSerializer):
    display_name = CharField()
    email = EmailField(validators=[UniqueValidator(queryset=Outlet.objects.all())])

    class Meta:
        model = Outlet
        fields = ['display_name', 'opening_hours', 'closing_hours', 'country', 'city', 'street',
                  'longitude', 'latitude', 'location', 'time_zone', 'delivery_area', 'contact',
                  'slug', 'email', 'connected_email', 'image']


