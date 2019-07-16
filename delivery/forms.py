from django import forms

from delivery.models import DeliveryPolicy
from libs.mixins import SetOutletInFormMixin
from outlets.outlet_models import Outlet


class DeliveryPolicyForm(SetOutletInFormMixin, forms.ModelForm):
    class Meta:
        model = DeliveryPolicy
        fields = ['radius', 'delivery_time', 'price']

    def clean_price(self):
        price = self.cleaned_data['price']
        return round(price, 2)

    def save(self, commit=True):
        self.instance = super(DeliveryPolicyForm, self).save(commit=False)
        self.instance.outlet = self.outlet
        self.instance.currency = self.outlet.currency
        self.instance.save()
        return super(DeliveryPolicyForm, self).save()
