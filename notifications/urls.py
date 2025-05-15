from django.urls import path
from .views import NotificationAPIView


urlpatterns = [
    path('notify/', NotificationAPIView.as_view(), name='notify')
]
