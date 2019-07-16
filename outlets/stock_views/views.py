from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from libs.mixins import OutletContextForTemplatesMixin, OutletKwargForFormMixin, OutletPermissionCheckMixin
from outlets.forms import OutletStockAdminForm, OutletItemAdminForm

from outlets.stock_models import OutletStock, OutletItem


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

    def get_queryset(self):
        qs = super(DetailStock, self).get_queryset().filter(outlet=self.outlet)
        return qs


class AddStock(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, OutletKwargForFormMixin,
               CreateView):
    model = OutletStock
    form_class = OutletStockAdminForm
    template_name = 'outlets/stock/add_stock.html'

    def get_success_url(self):
        return reverse('outlets:stocks:detail', kwargs={'outlet_id': self.outlet.id, 'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(AddStock, self).get_context_data(**kwargs)
        context['item_form'] = OutletItemAdminForm(outlet=self.outlet)
        context['operation'] = 'add'

        return context


class AddItem(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, OutletKwargForFormMixin,
              CreateView):
    model = OutletItem
    form_class = OutletItemAdminForm
    template_name = 'outlets/stock/add_item.html'

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse(dict(value=self.object.id, label=str(self.object)))

    def form_invalid(self, form):
        messages.error(self.request,
                       "{}".format(form.errors))
        return redirect(reverse('outlets:stocks:add', kwargs=dict(outlet_id=self.outlet.id)))


class EditStock(OutletPermissionCheckMixin, OutletKwargForFormMixin, OutletContextForTemplatesMixin,
                UpdateView):
    model = OutletStock
    queryset = OutletStock.objects.all()
    form_class = OutletStockAdminForm
    template_name = 'outlets/stock/add_stock.html'

    def get_queryset(self):
        return super(EditStock, self).get_queryset().filter(outlet=self.outlet)

    def get_success_url(self):
        return reverse('outlets:stocks:detail', kwargs={'outlet_id': self.outlet.id, 'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EditStock, self).get_context_data(**kwargs)
        context['operation'] = 'Edit'
        return context


class DeleteStock(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, DeleteView):
    model = OutletStock
    queryset = OutletStock.objects.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request,
                         "{message} S.K.U - {sku}, {name}".format(
                             message="The stock has been deleted",
                             sku=self.object.sku,
                             name=self.object
                         ))
        return reverse('outlets:stocks:list', kwargs={'outlet_id': self.outlet.id})

