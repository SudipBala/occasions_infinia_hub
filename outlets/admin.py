from django.contrib import admin

# Register your models here.
from outlets.outlet_models import Outlet
from outlets.stock_models import Category, SubCategory, Item, Flavour, Size


# admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Item)
admin.site.register(Outlet)
admin.site.register(Flavour)
admin.site.register(Size)

