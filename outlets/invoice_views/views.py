from django.conf import settings
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from easy_pdf.views import PDFTemplateView

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


class PDFDetailInvoiceView(OutletPermissionCheckMixin, PDFTemplateView):
    model = OutletInvoice
    template_name = 'outlets/invoice/invoice_pdf.html'

    pk_url_kwarg = 'pk'
    base_url = 'file://' + settings.STATIC_ROOT

    def get_download_filename(self):
        return "Invoice #" + self.object.invoice_number + ".pdf"

    def get_object(self, **kwargs):
        try:
            self.object = OutletInvoice.objects.get(pk=kwargs.get(self.pk_url_kwarg))
            return self.object
        except OutletInvoice.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': OutletInvoice._meta.verbose_name})

    def get_context_data(self, **kwargs):
        self.get_object(**kwargs)
        context = super(PDFDetailInvoiceView, self).get_context_data(pagesize='A4',
                                                                title='Invoice #{}'.format(
                                                                    self.object.invoice_number),
                                                                **kwargs)
        context['object'] = self.object
        return context



#for user front end
class PDFInvoiceUserEndView(PDFTemplateView):
    model = OutletInvoice
    template_name = 'outlets/invoice/invoice_pdf.html'

    pk_url_kwarg = 'pk'
    base_url = 'file://' + settings.STATIC_ROOT

    def get_download_filename(self):
        return "Invoice #" + self.object.invoice_number + ".pdf"

    def get_object(self, **kwargs):
        try:
            self.object = OutletInvoice.objects.get(pk=kwargs.get(self.pk_url_kwarg))
            return self.object
        except OutletInvoice.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': OutletInvoice._meta.verbose_name})

    def get_context_data(self, **kwargs):
        self.get_object(**kwargs)
        context = super(PDFDetailInvoiceView, self).get_context_data(pagesize='A4',
                                                                     title='Invoice #{}'.format(
                                                                         self.object.invoice_number),
                                                                     **kwargs)
        context['object'] = self.object
        return context