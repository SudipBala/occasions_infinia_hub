
from django.urls import path


from social_app.views import RegistrationAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegistrationAPIView.as_view()),
]
