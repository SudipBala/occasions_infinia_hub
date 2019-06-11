from django.shortcuts import render
from django.views import View

from outlets.forms import OutletForm
from outlets.outlet_models import Outlet


class OutletsCreateView(View):

    def get(self, request):
        get_all_outlets = Outlet.objects.all()

        context = {'outlets': get_all_outlets}

        return render(request, 'outlets/create_outlet.html', context)

    def post(self, request):
        form = OutletForm(request.POST or None)
        if form.is_valid()():
            form.save()
        context = {'outlets': form}
        return render((request, 'outlets/create_outlet.html', context))

