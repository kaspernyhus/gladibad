from django.urls import path

from . import views

urlpatterns = [
    path('vip/', views.vip_index, name='vip_index'),
    path('notify_me', views.notify_me, name='notify_me'),
]