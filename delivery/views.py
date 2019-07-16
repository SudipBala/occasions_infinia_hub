from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from delivery.forms import DeliveryPolicyForm
from delivery.models import DeliveryPolicy
from libs.mixins import OutletPermissionCheckMixin, OutletContextForTemplatesMixin, OutletKwargForFormMixin
from outlets.forms import OutletItemAdminForm


class CreateDeliveryPolicy(OutletPermissionCheckMixin, OutletContextForTemplatesMixin,
                           OutletKwargForFormMixin, CreateView):
    model = DeliveryPolicy
    form_class = DeliveryPolicyForm
    template_name = 'delivery_policy/create_delivery_policy.html'

    def get_success_url(self):
        return reverse('outlets:delivery:list', kwargs={'outlet_id': self.outlet.id})


class ListDeliveryPolicy(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, ListView):
    model = DeliveryPolicy
    queryset = DeliveryPolicy.objects.all()
    paginate_by = 12
    template_name = 'delivery_policy/list_delivery_policy.html'

    def get_queryset(self):
        qs = super(ListDeliveryPolicy, self).get_queryset().filter(outlet=self.outlet)
        return qs

    def get_context_data(self, **kwargs):
        context = super(ListDeliveryPolicy, self).get_context_data(**kwargs)

        return context


class DetailDeliveryPolicy(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, DetailView):
    model = DeliveryPolicy
    queryset = DeliveryPolicy.objects.all()
    template_name = 'delivery_policy/detail_delivery_policy.html'

    def get_queryset(self):
        qs = super(DetailDeliveryPolicy, self).get_queryset().filter(outlet=self.outlet)
        return qs


class DeleteDeliveryPolicy(OutletPermissionCheckMixin, OutletContextForTemplatesMixin, DeleteView):
    model = DeliveryPolicy
    queryset = DeliveryPolicy.objects.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request,
                         "{message}".format(
                             message="The stock has been deleted",
                         ))
        return reverse('outlets:delivery:list', kwargs={'outlet_id': self.outlet.id})


class EditDeliveryPolicy(OutletPermissionCheckMixin, OutletKwargForFormMixin, OutletContextForTemplatesMixin,
                         UpdateView):
    model = DeliveryPolicy
    queryset = DeliveryPolicy.objects.all()
    form_class = DeliveryPolicyForm
    template_name = 'delivery_policy/create_delivery_policy.html'

    def get_queryset(self):
        return super(EditDeliveryPolicy, self).get_queryset().filter(outlet=self.outlet)

    def get_success_url(self):
        return reverse('outlets:delivery:list', kwargs={'outlet_id': self.outlet.id})

    def get_context_data(self, **kwargs):
        context = super(EditDeliveryPolicy, self).get_context_data(**kwargs)
        context['operation'] = 'Edit'
        return context
