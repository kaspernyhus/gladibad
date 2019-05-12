from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vip/', views.vip_index, name='vip_index'),
    path('changestate/<state>/', views.update_db, name='update_db'),
    path('stats/', views.stats, name='stats'),
    path('stats<int:entries_requested>/', views.stats, name='stats'),
    path('about', views.about, name='about'),
    path('notify_me<int:slack_user>/', views.notify_me, name="notify_me"),
]

