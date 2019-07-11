from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from libs.mixins import IsAdminUserMixin
from outlets.forms import OutletsAdminForm
from outlets.outlet_models import Outlet


class OutletCreate(CreateView):
    template_name = 'outlets/outlet/create_outlet.html'
    form_class = OutletsAdminForm
    queryset = Outlet.objects.all()

    def get_success_url(self):
        return reverse('outlets:outlet:list')


class OutletList(IsAdminUserMixin, ListView):
    template_name = "outlets/outlet/list_outlets.html"
    queryset = Outlet.objects.all()


class OutletDetail(DetailView):
    # model = Outlet
    # queryset = Outlet.objects.all()
    template_name = 'outlets/outlet/detail_outlet.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Outlet, id=id_)


class OutletUpdate(UpdateView):
    template_name = 'outlets/outlet/create_outlet.html'
    form_class = OutletsAdminForm
    queryset = Outlet.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Outlet, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('outlets:outlet:list')


class OutletDelete(DeleteView):
    model = Outlet
    queryset = Outlet.objects.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "{message}".format(
            message="The outlet has been deleted"
        ))
        return reverse('outlets:outlet:list')



