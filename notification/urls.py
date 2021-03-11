from notification.views import *
from django.urls import path
from notification.models import Notification
app_name = "notification"

urlpatterns = [
    path('', ShowNOtification, name="show_notification"),
    path('<noti_id>/delete/', DeleteNotification, name="delete_notification"),
]
