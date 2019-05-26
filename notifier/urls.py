from django.urls import path

from . import views

urlpatterns = [
    path('create_user/<user_name>/', views.create_slack_user, name='create_user'),
    path('notify_me<int:slack_user>/', views.notify_me, name="notify_me"),
]