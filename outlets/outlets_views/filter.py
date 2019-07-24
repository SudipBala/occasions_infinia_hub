import django_filters as df

from outlets.outlet_models import Outlet


class OutletFilter(df.FilterSet):

    class Meta:
        model = Outlet
        fields = ['country']

