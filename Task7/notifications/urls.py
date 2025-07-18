from django.urls import path
from .views import UserNotificationListView, UnreadNotificationCountView

urlpatterns = [
    path('', UserNotificationListView.as_view(), name='user-notifications'),
    path('unread-count/', UnreadNotificationCountView.as_view(), name='unread-notification-count'),
]
