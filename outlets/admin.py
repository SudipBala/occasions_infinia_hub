from django.contrib import admin

# Register your models here.
from outlets.models import Outlet
from outlets.stock_models import Category, Item

# admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Outlet)



