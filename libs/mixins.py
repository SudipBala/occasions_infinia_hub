from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.views.generic.base import View

from outlets.outlet_models import Outlet


class OutletPermissionCheckMixin(object):
    def dispatch(self, request, *args, **kwargs):
        outlet_id = kwargs.get('outlet_id')
        try:
            outlet = Outlet.objects.get(id=int(outlet_id))
        except (Outlet.DoesNotExist, ValueError):
            return JsonResponse({"Message": "Store ID missing."})

        self.outlet = outlet

        has_access = True
        #TODO checkpermission
        if has_access:
            return super(OutletPermissionCheckMixin, self).dispatch(request, *args, **kwargs)

        return JsonResponse({"Message": "Please login with proper email account assigned to your store."})


class OutletKwargForFormMixin(object):
    """
    pass outlet argument to the form
    """

    def get_form_kwargs(self):
        kwarg = super(OutletKwargForFormMixin, self).get_form_kwargs()
        kwarg['outlet'] = self.outlet
        return kwarg


class OutletContextForTemplatesMixin(object):
    """
    outlet and outlet_id are repeatedly passed to the templates as context.
    """

    def get_context_data(self, **kwargs):
        context = super(OutletContextForTemplatesMixin, self).get_context_data(**kwargs)
        context['outlet'] = self.outlet
        context['outlet_id'] = self.outlet.id
        return context


class SetOutletInFormMixin(object):
    def __init__(self, *args, **kwargs):
        self.outlet = kwargs.pop('outlet', None)
        super(SetOutletInFormMixin, self).__init__(*args, **kwargs)


class IsAdminUserMixin(UserPassesTestMixin, View):
    """checks if admin is superuser"""

    def test_func(self):
        return self.request.user.is_superuser
