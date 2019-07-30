from django.contrib import admin

# Register your models here.
from delivery.models import DeliveryPolicy, TrackingDetails

admin.site.register(DeliveryPolicy)
admin.site.register(TrackingDetails)
