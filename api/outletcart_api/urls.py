from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


app_name = 'outletcart_api'

urlpatterns = [
    path('outletcarts/<pk>/', views.OutletCartDetailView.as_view(), name='outletcart-detail' ),
    path('outletcarts/', views.OutletCartListView.as_view(), name="outletcart-list"),
]
urlpatterns=format_suffix_patterns(urlpatterns)

