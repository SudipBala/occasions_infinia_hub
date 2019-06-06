from django.forms import ModelForm

from outlets.outlet_models import Outlet


class OutletForm(ModelForm):
    class Meta:
        model = Outlet
        #
        exclude = ()



