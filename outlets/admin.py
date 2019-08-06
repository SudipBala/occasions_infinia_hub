from leaflet.admin import LeafletGeoAdmin
from outlets.models import OutletItemLine, OutletCart, ItemLineInvoice, OutletInvoice
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

admin.site.register(OutletItemLine)
admin.site.register(OutletCart)
admin.site.register(ItemLineInvoice)
admin.site.register(OutletInvoice)

