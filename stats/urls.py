from django.urls import path

from . import views

urlpatterns = [
    path('stats/', views.stats, name='stats'),
    path('stats<int:entries_requested>/', views.stats, name='stats'),
    path('more_stats/', views.more_stats, name='more_stats'),
    path('more_stats<int:entries_requested>/', views.more_stats, name='more_stats'),

]