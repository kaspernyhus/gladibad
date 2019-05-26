from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('changestate/<state>/', views.update_db, name='update_db'),
    path('about', views.about, name='about'),
]