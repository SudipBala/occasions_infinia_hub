from django.urls import path

from api.country_api.views import CountryAPIView, CountryOutletAPIView

app_name = 'country_api'
urlpatterns = [
    path('v1/country/', CountryAPIView.as_view(), name="country"),
    path('v1/<str:country>/outlets/', CountryOutletAPIView.as_view(), name="country_outlets")
]