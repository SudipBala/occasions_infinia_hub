from django.views.generic import DetailView

from libs.mixins import OutletPermissionCheckMixin, OutletKwargForFormMixin, OutletContextForTemplatesMixin
from outlets.models import OutletInvoice


class DetailInvoice(OutletPermissionCheckMixin, OutletKwargForFormMixin, OutletContextForTemplatesMixin, DetailView):
    model = OutletInvoice
    queryset = OutletInvoice.objects.all()
    template_name = 'outlets/invoice/invoice_detail.html'

    def get_queryset(self):
        return super(DetailInvoice, self).get_queryset().filter(associated_outlet=self.outlet)

    def get_context_data(self, **kwargs):
        context = super(DetailInvoice, self).get_context_data(**kwargs)
        return context
