from django.urls import path

from . import views

urlpatterns = [
    path('vip/', views.vip_index, name='vip_index'),
]