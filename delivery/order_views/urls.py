from django.urls import path, include

from delivery.order_views.views import ListOrders

app_name = 'delivery'

urlpatterns = [
    path('', ListOrders.as_view(), name='list'),
    path('invoices/', include(('outlets.invoice_views.urls', 'outlets'), namespace="invoice"))

]
