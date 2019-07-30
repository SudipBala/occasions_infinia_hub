from django.urls import path

from delivery.deliverypolicy_views.views import CreateDeliveryPolicy, ListDeliveryPolicy, DetailDeliveryPolicy, \
    DeleteDeliveryPolicy, EditDeliveryPolicy

app_name = 'delivery'

urlpatterns = [
    path('create/', CreateDeliveryPolicy.as_view(), name='create'),
    path('', ListDeliveryPolicy.as_view(), name='list'),
    path('<int:pk>/', DetailDeliveryPolicy.as_view(), name='detail'),
    path('<int:pk>/delete', DeleteDeliveryPolicy.as_view(), name='delete'),
    path('<int:pk>/update', EditDeliveryPolicy.as_view(), name='update')
]
