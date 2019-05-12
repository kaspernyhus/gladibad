from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('changestate/<state>/', views.update_db, name='update_db'),
    path('stats/', views.stats, name='stats'),
    path('stats<int:entries_requested>/', views.stats, name='stats'),
    path('about', views.about, name='about'),
]

