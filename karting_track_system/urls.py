"""karting_track_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, include
from karting_track_system import views
from django.conf import settings
from .views import (
    FacebookWebhookView,
    )

WEBHOOK_ENDPOINT = settings.WEBHOOK_ENDPOINT


urlpatterns = [
    path('home/',views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('records/', views.records, name = 'records'),
    path('statistics/', views.statistics, name = 'statistics'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('userprofile/', views.userProfile, name = 'userprofile'),
    path('control_races/', views.control_races, name= 'control_races'),
    re_path(r'^' + str(WEBHOOK_ENDPOINT) + '/$', FacebookWebhookView.as_view(), name='webhook'),
    path('',views.policy, name = 'policy'),
]
