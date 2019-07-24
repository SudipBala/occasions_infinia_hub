from leaflet.admin import LeafletGeoAdmin
from django.contrib import admin

from outlets.outlet_models import Outlet
from outlets.stock_models import Category, OutletItem, OutletStock


class OutletAdmin(LeafletGeoAdmin):
    list_display = ('display_name', 'location')


# admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(OutletItem)
admin.site.register(OutletStock)
admin.site.register(Outlet, OutletAdmin)
