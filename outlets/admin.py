from outlets.outlet_models import Outlet
from django.contrib import admin
from outlets.stock_models import Category, OutletItem, OutletStock


# admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(OutletItem)
admin.site.register(OutletStock)
admin.site.register(Outlet)



