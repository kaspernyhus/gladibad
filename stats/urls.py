from django.urls import path

from . import views

urlpatterns = [
    path('stats/', views.stats, name='stats'),
    path('stats<int:entries_requested>/', views.stats, name='stats'),
    path('gennemsnit/', views.averages, name='averages'),
    path('gennemsnit<int:entries_requested>/', views.averages, name='averages'),

]