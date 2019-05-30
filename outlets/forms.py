from django.forms import ModelForm

from outlets.models import Outlet


class OutletForm(ModelForm):
    class Meta:
        model = Outlet
        #
        exclude = ()



