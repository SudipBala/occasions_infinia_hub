from django.urls import path

from outlets.invoice_views.views import DetailInvoice, PDFDetailInvoiceView

urlpatterns = [
    path('<int:pk>/', DetailInvoice.as_view(), name='detail'),
    path('<int:pk>/pdf/', view=PDFDetailInvoiceView.as_view(), name="pdf"),

]
