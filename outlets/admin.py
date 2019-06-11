from django.contrib import admin

# Register your models here.

from outlets.outlet_models import Outlet
from outlets.stock_models import Category, BaseItem, OutletItem, OutletStock

# admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(OutletItem)
admin.site.register(OutletStock)
admin.site.register(Outlet)



