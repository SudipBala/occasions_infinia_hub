from rest_framework import serializers
from rest_framework.serializers import CharField, EmailField, ModelSerializer
from rest_framework.validators import UniqueValidator

from outlets.models import OfferBannerModel
from outlets.outlet_models import Outlet


class OfferBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferBannerModel
        fields = ['banner_image', 'offer_message', 'offer_discount']


class OutletDetailSerializer(serializers.ModelSerializer):
    display_name = CharField()
    email = EmailField(validators=[UniqueValidator(queryset=Outlet.objects.all())])

    class Meta:
        model = Outlet
        fields = "__all__"


class OutletSerializer(ModelSerializer):
    class Meta:
        model = Outlet
        fields = "__all__"
