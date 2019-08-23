from django import forms
from django.core.exceptions import ValidationError
from Occasions.settings import LEAFLET_CONFIG
from libs.mixins import SetOutletInFormMixin
from outlets.category_models import Category
from outlets.outlet_models import Outlet
from outlets.stock_models import OutletStock, OutletItem
from django.contrib.gis.forms import OSMWidget, PointField, ModelForm


class OutletForm(forms.ModelForm):
    class Meta:
        model = Outlet
        #
        exclude = ()


class OutletItemAdminForm(SetOutletInFormMixin, forms.ModelForm):
    class Meta:
        model = OutletItem
        fields = ['type1', 'type2', 'display_name', 'quantity', 'unit', 'image']

    def __init__(self, *args, **kwargs):
        super(OutletItemAdminForm, self).__init__(*args, **kwargs)


class OutletStockAdminForm(forms.ModelForm):
    digits = 13

    class Meta:
        model = OutletStock
        fields = ['country', 'brand', 'item', 'sku', 'available',
                  'price', 'currency', 'description',
                  'maximum_quantity', 'minimum_quantity',
                  'extra']

    def clean_available(self):
        if not self.cleaned_data["available"]:
            return 0
        return self.cleaned_data["available"]

    def clean_image(self):
        # if not self.cleaned_data["available"]:
        #     return 0
        return self.cleaned_data["image"]

    def clean_minimum_quantity(self):
        if not self.cleaned_data["minimum_quantity"]:
            return 0
        return self.cleaned_data["minimum_quantity"]

    def clean_maximum_and_minimum_quantity(self):
        maximum_quantity = self.cleaned_data.get('maximum_quantity', None)
        # can be None
        if maximum_quantity and self.cleaned_data['minimum_quantity'] > maximum_quantity:
            raise ValidationError({"maximum_quantity": "maximum quantity must be bigger than minimum quantity."},
                                  code="MaxQtyGreaterThanMinQty")

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if not sku.isdigit():
            raise ValidationError('Code can only contain numbers. Restricted to {} digits.'.format(self.digits))
        sku = sku[:self.digits]
        return sku

    def clean(self):
        cleaned_data = super(OutletStockAdminForm, self).clean()
        self.clean_maximum_and_minimum_quantity()
        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        return round(price, 2)

    def __init__(self, *args, **kwargs):
        self.outlet = kwargs.pop('outlet', None)
        self.request = kwargs.pop('request', None)  # fixme
        self.currency = self.outlet.currency
        super(OutletStockAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.id:
            self.fields['item'].queryset = self.fields['item'].queryset.filter(id=self.instance.item.id)
            self.initial['sku'] = self.instance.sku[:-1]
        else:
            if not kwargs.get('data'):  # get form else is post form
                self.fields['item'].queryset = self.fields['item'].queryset.none()

    def save(self, commit=True):
        self.instance = super(OutletStockAdminForm, self).save(commit=False)
        self.instance.outlet = self.outlet
        self.instance.currency = self.currency
        if self.request and 'stock_id' in self.request.GET:
            stock = OutletStock.objects.get(id=self.request.GET['stock_id'])
            self.instance.image = stock.image
            self.instance.save()
        return super(OutletStockAdminForm, self).save()


class OutletsAdminForm(forms.ModelForm):
    class Meta:
        model = Outlet
        fields = ['display_name', 'opening_hours', 'closing_hours', 'country', 'city', 'street',
                  'location', 'time_zone', 'delivery_area', 'contact',
                  'slug', 'email', 'connected_email', 'image']
        widgets = {
            'location': OSMWidget(
                attrs={
                    'map_width': '100%',
                    'map_height': 500,
                    'default_lat': 27.7172,
                    'default_lon': 85.3240,
                    'default_zoom': 16

                })}

    def clean_image(self):
        return self.cleaned_data['image']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
