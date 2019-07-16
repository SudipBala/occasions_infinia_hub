from django.contrib import admin

# Register your models here.
from delivery.models import DeliveryPolicy

admin.site.register(DeliveryPolicy)
