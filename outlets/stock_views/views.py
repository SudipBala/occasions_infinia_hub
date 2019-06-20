from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from libs.mixins import OutletContextForTemplatesMixin, OutletKwargForFormMixin, OutletPermissionCheckMixin
from outlets.forms import OutletStockAdminForm

from outlets.stock_models import OutletStock


class ListStock(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, ListView):
    model = OutletStock
    queryset = OutletStock.objects.all()
    paginate_by = 12
    template_name = "outlets/stock/list_stocks.html"

    def get_queryset(self):
        qs = super(ListStock, self).get_queryset().filter(outlet=self.outlet)
        # self.filter = StocksFilter(self.request.GET, queryset=qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListStock, self).get_context_data(**kwargs)
        # context['type2'] = self.outlet.get_category_templates(1)
        # context['type3'] = self.outlet.get_category_templates(2)
        # context['filter'] = self.filter
        return context


class DetailStock(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, DetailView):
    model = OutletStock
    queryset = OutletStock.objects.all()
    template_name = 'outlets/stock/detail_stock.html'

#addstock
#additem
#updateitem
#deleteitem
