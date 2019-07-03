from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from outlets.forms import OutletForm
from outlets.outlet_models import Outlet
from outlets.stock_models import BaseItem


class OutletsCreateView(View):

    def get(self, request):
        get_all_outlets = Outlet.objects.all()

        context = {'outlets': get_all_outlets}

        return render(request, 'outlets/outlet/create_outlet.html', context)

    def post(self, request):
        form = OutletForm(request.POST or None)
        if form.is_valid()():
            form.save()
        context = {'outlets': form}
        return render((request, 'outlets/outlet/create_outlet.html', context))


def outlet_create_view(request):
    form = OutletForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "outlets/outlet/create_outlet.html", context)


def outlet_list_view(request):
    qs = Outlet.objects.all()
    template_name = "outlets/outlet/list_outlets.html"
    context = {'object_list': qs}
    return render(request, template_name, context)


# class ItemList(ListView):
#     model = BaseItem
#     fields = '__all__'
#
#
# class ItemDetail(DetailView):
#     model = BaseItem
#
#
# class ItemCreate(CreateView):
#     model = BaseItem
#     fields = '__all__'
#
#
# class ItemUpdate(UpdateView):
#     model = BaseItem
#     fields = '__all__'
#
#
# class ItemDelete(DeleteView):
#     model = BaseItem
#     fields = '__all__'
