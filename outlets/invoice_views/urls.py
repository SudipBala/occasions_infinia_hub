from django.urls import path

from outlets.invoice_views.views import DetailInvoice

urlpatterns = [
    path('<int:pk>/', DetailInvoice.as_view(), name='detail')
]
