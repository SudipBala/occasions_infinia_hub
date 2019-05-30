from django.shortcuts import render


# Create your views here.
from outlets.forms import OutletForm


def outlet_create_view(request):
    form = OutletForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "outlets/create_outlet.html", context)
