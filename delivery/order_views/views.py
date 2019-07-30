from django.views.generic import ListView
from shutil import copy

from delivery.models import TrackingDetails
from delivery.order_views.filters import TrackingDetailsFilter
from libs.constants import STATUS_CHOICES
from libs.mixins import OutletPermissionCheckMixin, OutletContextForTemplatesMixin, OutletKwargForFormMixin


class ListOrders(OutletPermissionCheckMixin, OutletKwargForFormMixin,
                 OutletContextForTemplatesMixin, ListView):
    model = TrackingDetails
    template_name = 'orders/list_orders.html'
    paginate_by = 12
    queryset = TrackingDetails.objects.all()

    def get_queryset(self):
        queryset = super(ListOrders, self).get_queryset().filter(order__associated_outlet=self.outlet). \
            order_by('-order_placed')
        return TrackingDetailsFilter(self.request.GET,
                                     queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super(ListOrders, self).get_context_data(**kwargs)
        context['status_choices'] = STATUS_CHOICES
        if 'page' in self.request.GET:
            request_clone = copy(self.request)
            request_clone.GET._mutable = True
            del request_clone.GET['page']
            request_clone.GET._mutable = False
            context['request'] = request_clone
        return context

