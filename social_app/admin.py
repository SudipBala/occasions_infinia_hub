from django.contrib import admin

from social_app.forms import ShippingForm
from .models import OccasionUser, ShippingAddress


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'backend')
    pass


class ShippingAddressAdmin(admin.ModelAdmin):
    form = ShippingForm


admin.site.register(OccasionUser, UserAdmin)
admin.site.register(ShippingAddress, ShippingAddressAdmin)

# SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
