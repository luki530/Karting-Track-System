from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'aghart-home'),
    path('records/', views.records, name = 'aghart-records'),
    path('statistics/', views.statistics, name = 'aghart-statistics')
]
