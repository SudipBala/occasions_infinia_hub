import django_filters as df

from delivery.models import DeliveryPolicy


class DeliveryFilter(df.FilterSet):
    price__gt = df.NumberFilter(field_name='price', lookup_expr='gte')

    class Meta:
        model = DeliveryPolicy
        fields = ['outlet', 'currency']
        exclude = []
