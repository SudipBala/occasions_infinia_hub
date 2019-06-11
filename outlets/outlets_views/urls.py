
from django.urls import path

from outlets.outlets_views.views import OutletsCreateView

urlpatterns = [
    # path('create/', outlet_create_view, name="list_outlets")

    path('list/', OutletsCreateView.as_view(), name="list_outlets")
]