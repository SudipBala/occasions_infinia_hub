import django_filters as df

from delivery.models import TrackingDetails


class TrackingDetailsFilter(df.FilterSet):
    class Meta:
        model = TrackingDetails
        fields = ['order', 'status', 'order_placed', 'shipped_to']
