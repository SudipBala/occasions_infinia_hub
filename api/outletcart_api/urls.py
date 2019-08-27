from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


appname='outletcart_api'
urlpatterns=[
    path('outletcart/<int:pk>/',views.OutletCartDetailView.as_view(), name='outletcart-detail' ),
    path('outletcart/', views.OutletCartListView.as_view(), name="outletcart-list")
]
urlpatterns=format_suffix_patterns(urlpatterns)